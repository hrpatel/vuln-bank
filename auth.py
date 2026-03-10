from flask import jsonify, request
import jwt
import datetime
from functools import wraps

# Vulnerable JWT implementation with common security issues

# Weak secret key (CWE-326)
JWT_SECRET = "secret123"

# Vulnerable algorithm selection - allows 'none' algorithm
ALGORITHMS = ['HS256', 'none']

def generate_token(user_id, username, is_admin=False):
    """
    Generate a JWT token with weak implementation
    Vulnerability: No token expiration (CWE-613)
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'is_admin': is_admin,
        # Missing 'exp' claim - tokens never expire
        'iat': datetime.datetime.utcnow()
    }
    
    # Vulnerability: Using a weak secret key
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def verify_token(token):
    """
    Verify JWT token with multiple vulnerabilities
    - Accepts 'none' algorithm (CWE-347)
    - No signature verification in some cases
    - No expiration check
    """
    try:
        # Vulnerability: Accepts any algorithm, including 'none'
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHMS)
        return payload
    except jwt.exceptions.InvalidSignatureError:
        # Vulnerability: Still accepts tokens in some error cases
        try:
            # Second try without verification
            payload = jwt.decode(token, options={'verify_signature': False})
            return payload
        except:
            return None
    except Exception as e:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Try to get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Handle 'Bearer' token format
                if 'Bearer' in auth_header:
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
            except IndexError:
                token = None
                
        # Vulnerability: Multiple token locations (token hijacking risk)
        # Also check query parameters (vulnerable by design)
        if not token and 'token' in request.args:
            token = request.args['token']
            
        # Also check form data (vulnerable by design)
        if not token and 'token' in request.form:
            token = request.form['token']
            
        # Also check cookies (vulnerable by design)
        if not token and 'token' in request.cookies:
            token = request.cookies['token']
            
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            current_user = verify_token(token)
            if current_user is None:
                return jsonify({'error': 'Invalid token'}), 401
                
            # Vulnerability: No token expiration check
            return f(current_user, *args, **kwargs)
            
        except Exception as e:
            # Vulnerability: Detailed error exposure
            return jsonify({
                'error': 'Invalid token', 
                'details': str(e)
            }), 401
            
    return decorated

# New API endpoints with JWT authentication
def init_auth_routes(app):
    from database import execute_query

    @app.route('/api/login', methods=['POST'])
    def api_login():
        auth = request.get_json()
        
        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'error': 'Missing credentials'}), 401
            
        # T38: Use parameterized query to prevent SQL injection
        result = execute_query(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (auth.get('username'), auth.get('password'))
        )
        user = result[0] if result else None
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Generate token
        token = generate_token(user[0], user[1], user[5])
        
        # Vulnerability: Exposed sensitive data in response
        return jsonify({
            'token': token,
            'user_id': user[0],
            'username': user[1],
            'account_number': user[3],
            'is_admin': user[5],
            'debug_info': {
                'login_time': str(datetime.datetime.now()),
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            }
        })

    @app.route('/api/check_balance', methods=['GET'])
    @token_required
    def api_check_balance(current_user):
        # Vulnerability: No additional authorization check
        # Any valid token can check any account balance
        account_number = request.args.get('account_number')
        
        result = execute_query(
            "SELECT username, balance FROM users WHERE account_number = %s",
            (account_number,)
        )
        user = result[0] if result else None
        
        if user:
            return jsonify({
                'username': user[0],
                'balance': user[1],
                'checked_by': current_user['username']
            })
        return jsonify({'error': 'Account not found'}), 404

    @app.route('/api/transfer', methods=['POST'])
    @token_required
    def api_transfer(current_user):
        data = request.get_json()
        
        if not data or not data.get('to_account') or not data.get('amount'):
            return jsonify({'error': 'Missing transfer details'}), 400
            
        # Vulnerability: No amount validation
        amount = float(data.get('amount'))
        to_account = data.get('to_account')
        
        
        # T38: Parameterized queries for transfer (race condition remains for training)
        result = execute_query(
            "SELECT balance FROM users WHERE id = %s",
            (current_user['user_id'],)
        )
        balance = result[0][0]
        
        if balance >= amount:
            execute_query(
                "UPDATE users SET balance = balance - %s WHERE id = %s",
                (amount, current_user['user_id']),
                fetch=False
            )
            execute_query(
                "UPDATE users SET balance = balance + %s WHERE account_number = %s",
                (amount, to_account),
                fetch=False
            )
            result = execute_query(
                "SELECT username, balance FROM users WHERE account_number = %s",
                (to_account,)
            )
            recipient = result[0]
            
            return jsonify({
                'status': 'success',
                'new_balance': balance - amount,
                'recipient': recipient[0],
                'recipient_new_balance': recipient[1]
            })
            
        return jsonify({'error': 'Insufficient funds'}), 400