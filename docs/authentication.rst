Authentication Guide
====================

This guide explains how authentication works in the Project Management API using JSON Web Tokens (JWT).

Overview
--------

The API uses **JWT-based authentication** with two types of tokens:

* **Access Token** - Short-lived (1 hour), used for API requests
* **Refresh Token** - Long-lived (30 days), used to obtain new access tokens

This approach provides:

* **Stateless authentication** - No server-side session storage required
* **Scalability** - Easy horizontal scaling without session management
* **Security** - Short-lived tokens limit exposure if compromised
* **Convenience** - Long-lived refresh tokens avoid frequent re-authentication

Authentication Flow
-------------------

Registration Flow
~~~~~~~~~~~~~~~~~

.. code-block:: text

   1. Client sends registration request
      POST /auth/register
      {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "SecurePass123",
        "user_type": "manager"
      }

   2. Server validates input
      - Email format
      - Password length (minimum 6 characters)
      - Email uniqueness

   3. Server hashes password using bcrypt
      - Automatic salt generation
      - Secure one-way hashing

   4. Server creates user in database

   5. Server generates JWT tokens
      - Access token (1 hour expiration)
      - Refresh token (30 days expiration)

   6. Server responds with tokens and user data
      {
        "access_token": "eyJhbGci...",
        "refresh_token": "eyJhbGci...",
        "user": {...}
      }

   7. Client stores tokens securely
      - LocalStorage (web)
      - Secure storage (mobile)
      - Encrypted cookies

Login Flow
~~~~~~~~~~

.. code-block:: text

   1. Client sends login request
      POST /auth/login
      {
        "email": "john@example.com",
        "password": "SecurePass123"
      }

   2. Server looks up user by email

   3. Server verifies password
      - Uses bcrypt.checkpw()
      - Compares hashed passwords

   4. If valid, server generates tokens
      - New access token
      - New refresh token

   5. Server responds with tokens
      {
        "access_token": "eyJhbGci...",
        "refresh_token": "eyJhbGci...",
        "user": {...}
      }

   6. Client stores tokens

Making Authenticated Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   1. Client includes access token in header
      Authorization: Bearer eyJhbGci...

   2. Server extracts token from header

   3. Server validates token
      - Verifies signature using SECRET_KEY
      - Checks expiration time
      - Extracts user_id from payload

   4. Server loads user from database

   5. Server processes request with user context

   6. Server responds with requested data

Token Refresh Flow
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   1. Access token expires (after 1 hour)

   2. Client receives 401 Unauthorized

   3. Client sends refresh request
      POST /auth/refresh
      {
        "refresh_token": "eyJhbGci..."
      }

   4. Server validates refresh token
      - Verifies signature
      - Checks expiration (30 days)

   5. Server generates new access token

   6. Server responds with new token
      {
        "access_token": "eyJhbGci..."
      }

   7. Client retries original request with new token

JWT Token Structure
-------------------

Access Token Payload
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "user_id": 1,
     "email": "john@example.com",
     "user_type": "manager",
     "type": "access",
     "iat": 1705315800,
     "exp": 1705319400
   }

**Fields:**

* ``user_id`` - Database ID of the user
* ``email`` - User's email address
* ``user_type`` - Role: "manager" or "employee"
* ``type`` - Token type: "access" or "refresh"
* ``iat`` - Issued at timestamp
* ``exp`` - Expiration timestamp

Refresh Token Payload
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "user_id": 1,
     "type": "refresh",
     "iat": 1705315800,
     "exp": 1707907800
   }

**Differences from access token:**

* No email or user_type (minimal payload)
* Longer expiration (30 days vs 1 hour)
* Only used for obtaining new access tokens

Token Signing
~~~~~~~~~~~~~

Tokens are signed using the **HS256 algorithm** (HMAC with SHA-256):

.. code-block:: python

   jwt.encode(payload, SECRET_KEY, algorithm='HS256')

The ``SECRET_KEY`` must be:

* **Long and random** (at least 32 characters)
* **Kept secret** (never commit to version control)
* **Unique per environment** (different for dev/staging/prod)

Generate a secure key:

.. code-block:: bash

   python -c "import secrets; print(secrets.token_hex(32))"

Authorization and Roles
-----------------------

Role Types
~~~~~~~~~~

**Manager**
  * Full access to all endpoints
  * Can create, update, and delete users
  * Can create, update, and delete projects
  * Can create, update, and delete tasks

**Employee**
  * Read access to users and projects
  * Can create, update, and delete tasks
  * Cannot modify users or projects

Permission Matrix
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Endpoint
     - Public
     - Employee
     - Manager
   * - POST /auth/register
     - ✓
     - ✓
     - ✓
   * - POST /auth/login
     - ✓
     - ✓
     - ✓
   * - GET /auth/verify
     -
     - ✓
     - ✓
   * - POST /users
     -
     -
     - ✓
   * - GET /users
     -
     - ✓
     - ✓
   * - PUT /users/<id>
     -
     -
     - ✓
   * - DELETE /users/<id>
     -
     -
     - ✓
   * - POST /projects
     -
     -
     - ✓
   * - GET /projects
     - ✓
     - ✓
     - ✓
   * - PUT /projects/<id>
     -
     -
     - ✓
   * - DELETE /projects/<id>
     -
     -
     - ✓
   * - POST /tasks
     -
     - ✓
     - ✓
   * - GET /tasks
     -
     - ✓
     - ✓
   * - PUT /tasks/<id>
     -
     - ✓
     - ✓
   * - DELETE /tasks/<id>
     -
     - ✓
     - ✓

Implementation with Decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The API uses two decorators for authorization:

**@token_required**
  Validates JWT token and loads user into Flask's ``g`` object:

  .. code-block:: python

     @app.route('/users')
     @token_required
     def get_users():
         current_user = get_current_user()
         # ... endpoint logic

**@manager_required**
  Validates token AND checks for manager role:

  .. code-block:: python

     @app.route('/users', methods=['POST'])
     @manager_required
     def create_user():
         # Only managers can access this
         # ... endpoint logic

Implementation Examples
-----------------------

Python with Requests
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests

   BASE_URL = 'http://localhost:5000'

   # Register
   response = requests.post(f'{BASE_URL}/auth/register', json={
       'name': 'John Doe',
       'email': 'john@example.com',
       'password': 'SecurePass123',
       'user_type': 'manager'
   })
   data = response.json()
   access_token = data['access_token']
   refresh_token = data['refresh_token']

   # Make authenticated request
   headers = {'Authorization': f'Bearer {access_token}'}
   response = requests.get(f'{BASE_URL}/users', headers=headers)
   users = response.json()

   # Refresh token
   response = requests.post(f'{BASE_URL}/auth/refresh', json={
       'refresh_token': refresh_token
   })
   new_access_token = response.json()['access_token']

JavaScript with Fetch
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   const BASE_URL = 'http://localhost:5000';

   // Register
   const registerResponse = await fetch(`${BASE_URL}/auth/register`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       name: 'John Doe',
       email: 'john@example.com',
       password: 'SecurePass123',
       user_type: 'manager'
     })
   });
   const { access_token, refresh_token, user } = await registerResponse.json();

   // Store tokens
   localStorage.setItem('access_token', access_token);
   localStorage.setItem('refresh_token', refresh_token);

   // Make authenticated request
   const usersResponse = await fetch(`${BASE_URL}/users`, {
     headers: {
       'Authorization': `Bearer ${access_token}`
     }
   });
   const users = await usersResponse.json();

   // Refresh token
   const refreshResponse = await fetch(`${BASE_URL}/auth/refresh`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ refresh_token })
   });
   const { access_token: newAccessToken } = await refreshResponse.json();

cURL Examples
~~~~~~~~~~~~~

.. code-block:: bash

   # Register
   curl -X POST http://localhost:5000/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "password": "SecurePass123",
       "user_type": "manager"
     }'

   # Login
   curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "SecurePass123"
     }'

   # Use access token
   curl -X GET http://localhost:5000/users \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

   # Refresh token
   curl -X POST http://localhost:5000/auth/refresh \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'

Security Best Practices
-----------------------

Token Storage
~~~~~~~~~~~~~

**Web Applications:**

* **Don't** store in localStorage if XSS is a concern
* **Do** use httpOnly cookies for sensitive apps
* **Do** use secure flag with HTTPS
* **Consider** using sessionStorage for more security

**Mobile Applications:**

* **Use** platform-specific secure storage (Keychain on iOS, Keystore on Android)
* **Don't** store in plain text files
* **Don't** log tokens in debug mode

Token Transmission
~~~~~~~~~~~~~~~~~~

* **Always** use HTTPS in production
* **Never** send tokens in URL query parameters
* **Always** use Authorization header
* **Consider** additional encryption for highly sensitive data

Token Lifecycle
~~~~~~~~~~~~~~~

* **Implement** automatic token refresh
* **Handle** token expiration gracefully
* **Clear** tokens on logout
* **Rotate** refresh tokens periodically
* **Revoke** tokens on password change (future enhancement)

Password Security
~~~~~~~~~~~~~~~~~

* **Minimum** 6 characters (consider increasing to 8-12)
* **Use** bcrypt for hashing (already implemented)
* **Don't** store plain text passwords
* **Consider** password complexity requirements
* **Implement** rate limiting on login attempts

Error Handling
--------------

Common Error Scenarios
~~~~~~~~~~~~~~~~~~~~~~

**Missing Token:**

.. code-block:: json

   {
     "error": "Authorization token is required"
   }

**Invalid Token:**

.. code-block:: json

   {
     "error": "Invalid token"
   }

**Expired Token:**

.. code-block:: json

   {
     "error": "Token has expired"
   }

**Insufficient Permissions:**

.. code-block:: json

   {
     "error": "Manager role required"
   }

Client-Side Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   async function makeAuthenticatedRequest(url) {
     let token = localStorage.getItem('access_token');

     let response = await fetch(url, {
       headers: { 'Authorization': `Bearer ${token}` }
     });

     if (response.status === 401) {
       // Token expired, try to refresh
       const refreshToken = localStorage.getItem('refresh_token');
       const refreshResponse = await fetch('/auth/refresh', {
         method: 'POST',
         body: JSON.stringify({ refresh_token: refreshToken })
       });

       if (refreshResponse.ok) {
         const { access_token } = await refreshResponse.json();
         localStorage.setItem('access_token', access_token);

         // Retry original request
         response = await fetch(url, {
           headers: { 'Authorization': `Bearer ${access_token}` }
         });
       } else {
         // Refresh failed, redirect to login
         window.location.href = '/login';
       }
     }

     return response.json();
   }

Testing Authentication
----------------------

Using pytest
~~~~~~~~~~~~

.. code-block:: python

   def test_authentication(client):
       # Register
       response = client.post('/auth/register', json={
           'name': 'Test User',
           'email': 'test@example.com',
           'password': 'password123',
           'user_type': 'employee'
       })
       assert response.status_code == 201
       data = response.get_json()
       assert 'access_token' in data

       # Use token
       token = data['access_token']
       response = client.get('/users', headers={
           'Authorization': f'Bearer {token}'
       })
       assert response.status_code == 200

Using Postman
~~~~~~~~~~~~~

1. **Register/Login** to get tokens
2. **Create environment variable** for ``access_token``
3. **Set up pre-request script** for automatic token refresh
4. **Use** ``{{access_token}}`` in Authorization header

Next Steps
----------

* Explore the :doc:`api_overview` for all available endpoints
* Review :doc:`design_rationale` for security decisions
* Check the :doc:`installation` guide for setup instructions
* Import the Postman collection for interactive testing
