# SDElements Profile and Key Assumptions — vuln-bank

**Project:** vuln-bank (SDElements ID: 31763)  
**Last updated:** March 10, 2026

---

## Selected profile

**Django Project (P5)**

- **Rationale:** Vuln-bank is a **Python web application** (Flask). The Django Project profile is the only Python-based web app profile in the SDElements library and is the closest match to our stack (Python, web UI, server-side rendering, REST APIs). Django and Flask share the same language and similar security concerns (auth, sessions, SQL, templates).
- **What it includes (baseline):** Web application component, Django/Python-oriented answers (A1061, A740, A1078, A4, A697, A707), which bring in requirements and development tasks for web applications and Python frameworks.

---

## Key assumptions (biased toward sensitive data, auth, encryption, compliance)

These survey answers were explicitly added so that the project is treated as handling sensitive data, using authentication and encryption, and having authorization and password management. This maximizes coverage of security tasks in those areas.

| Area | Assumption | Survey answer(s) |
|------|------------|-------------------|
| **Authentication** | Application authenticates users with passwords (no SSO). | Uses passwords (A19) |
| **Authentication** | Application has a “change password” feature. | Has change existing password function (A43) |
| **Authorization** | Application has features or data restricted by user/role. | Authorizes Subjects — Yes (A23) |
| **Session management** | Application uses session IDs (e.g. cookies) for authenticated state. | Has Session Management — Yes (A37) |
| **Encryption** | Passwords or secrets appear in configuration (e.g. DB, API keys). | Passwords stored in configuration files (A21) |
| **Encryption** | Application uses encryption in addition to SSL (e.g. stored data, tokens). | Uses encryption functions (not including SSL) (A27) |
| **Sensitive data / backend** | Application uses a SQL database (accounts, balances, PII). | Stand-alone database that supports SQL (A11) |
| **Architecture** | Application exposes REST/API (aligns with auth and data access). | Web service (A6) |

**Regulatory / compliance (assumed, not survey-driven):**

- **Financial / banking context:** The app is a banking demo (accounts, balances, transfers). Assumptions:
  - It should be treated as handling **financial and PII-like data**.
  - Controls relevant to **authentication, access control, encryption, and audit** are in scope.
- **No specific regulation** (e.g. PCI-DSS, GDPR) was selected in the survey; the bias is applied by the chosen profile and the answers above so that auth, encryption, and sensitive-data tasks are included. If your organization maps vuln-bank to a specific regulation, add the corresponding SDElements regulation/answer when available.

---

## Summary

- **Profile:** **Django Project (P5)** — selected as the best match for a Python (Flask) web application.
- **Assumptions:** Passwords and session-based auth; authorization (subject-based access); SQL database; passwords/secrets in config; use of encryption beyond SSL; change-password and web/API usage. Together, these bias the project toward **sensitive data handling, authentication, encryption, and controls relevant to compliance** without tying to one specific regulation.
- **Outcome:** With this profile and these answers, the project has **38 risk-relevant countermeasures** (vs. 1 with the Blank profile), including requirements such as “Secure the password reset mechanism” and other auth/session/encryption-related tasks.
