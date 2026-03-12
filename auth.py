from flask import jsonify, request
import jwt
import datetime
import os
import time
from functools import wraps
from collections import defaultdict

# Vulnerable JWT implementation with common security issues

# T76: Use env for JWT secret; fallback for dev/training only
JWT_SECRET = os.environ.get('JWT_SECRET') or os.environ.get('FLASK_SECRET_KEY') or 'secret123'

# T70: Account lockout after N failed attempts (in-memory; per username)
LOGIN_FAILURE_MAX = int(os.environ.get('LOGIN_FAILURE_MAX', 5))
LOGIN_LOCKOUT_SECONDS = int(os.environ.get('LOGIN_LOCKOUT_SECONDS', 900))  # 15 min
_login_failures = defaultdict(lambda: (0, 0.0))  # username -> (count, lock_until timestamp)

def _is_locked(username):
    count, lock_until = _login_failures[username]
    if lock_until and time.time() < lock_until:
        return True, lock_until
    if time.time() >= lock_until:
        _login_failures[username] = (0, 0.0)
    return False, None

def _record_failure(username):
    count, lock_until = _login_failures[username]
    if lock_until and time.time() >= lock_until:
        count, lock_until = 0, 0.0
    count += 1
    lock_until = time.time() + LOGIN_LOCKOUT_SECONDS if count >= LOGIN_FAILURE_MAX else 0.0
    _login_failures[username] = (count, lock_until if count >= LOGIN_FAILURE_MAX else 0.0)
    return count >= LOGIN_FAILURE_MAX

def _clear_failures(username):
    _login_failures[username] = (0, 0.0)

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
        auth_data = request.get_json()
        
        if not auth_data or not auth_data.get('username') or not auth_data.get('password'):
            return jsonify({'error': 'Missing credentials'}), 401

        username = auth_data.get('username')
        # T70: Account lockout - reject if locked
        locked, lock_until = _is_locked(username)
        if locked:
            return jsonify({
                'error': 'Account temporarily locked due to too many failed attempts',
                'retry_after': int(lock_until - time.time())
            }), 429
            
        # Vulnerability: SQL Injection still possible here
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{auth_data.get('password')}'"
        result = execute_query(query)
        user = result[0] if result else None
        
        if not user:
            _record_failure(username)
            return jsonify({'error': 'Invalid credentials'}), 401

        _clear_failures(username)
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
        
        result = execute_query(f"SELECT username, balance FROM users WHERE account_number='{account_number}'")
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
        
        
        # Vulnerability: Race condition in transfer
        result = execute_query(f"SELECT balance FROM users WHERE id={current_user['user_id']}")
        balance = result[0][0]
        
        if balance >= amount:
            # Vulnerability: SQL injection possible in to_account
            execute_query(f"UPDATE users SET balance = balance - {amount} WHERE id={current_user['user_id']}", fetch=False)
            execute_query(f"UPDATE users SET balance = balance + {amount} WHERE account_number='{to_account}'", fetch=False)
            
            # Vulnerability: Information disclosure
            result = execute_query(f"SELECT username, balance FROM users WHERE account_number='{to_account}'")
            recipient = result[0]
            
            return jsonify({
                'status': 'success',
                'new_balance': balance - amount,
                'recipient': recipient[0],
                'recipient_new_balance': recipient[1]
            })
            
        return jsonify({'error': 'Insufficient funds'}), 400