API Overview
============

This document provides a comprehensive overview of all API endpoints, request/response formats, and usage examples.

Base URL
--------

.. code-block:: text

   http://localhost:5000

Response Format
---------------

All responses are in JSON format with appropriate HTTP status codes.

Success Response
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "id": 1,
     "name": "Example Project",
     "created_at": "2025-01-15T10:30:00Z"
   }

Error Response
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Error message description"
   }

HTTP Status Codes
-----------------

* ``200 OK`` - Request successful
* ``201 Created`` - Resource created successfully
* ``400 Bad Request`` - Invalid input data
* ``401 Unauthorized`` - Missing or invalid authentication token
* ``403 Forbidden`` - Insufficient permissions
* ``404 Not Found`` - Resource not found
* ``500 Internal Server Error`` - Server error

Pagination
----------

List endpoints support pagination using query parameters:

* ``limit`` - Number of items to return (default varies by endpoint)
* ``offset`` - Number of items to skip (default: 0)

Example:

.. code-block:: bash

   GET /projects?limit=10&offset=20

Authentication Endpoints
------------------------

POST /auth/register
~~~~~~~~~~~~~~~~~~~

Register a new user account.

**Request:**

.. code-block:: http

   POST /auth/register HTTP/1.1
   Content-Type: application/json

   {
     "name": "John Doe",
     "email": "john@example.com",
     "password": "SecurePass123",
     "user_type": "manager"
   }

**Parameters:**

* ``name`` (string, required) - User's full name
* ``email`` (string, required) - Valid email address
* ``password`` (string, required) - Password (minimum 6 characters)
* ``user_type`` (string, optional) - Either "manager" or "employee" (default: "employee")

**Response (201 Created):**

.. code-block:: json

   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": 1,
       "name": "John Doe",
       "email": "john@example.com",
       "user_type": "manager",
       "created_at": "2025-01-15T10:30:00Z",
       "updated_at": "2025-01-15T10:30:00Z"
     }
   }

POST /auth/login
~~~~~~~~~~~~~~~~

Authenticate and receive JWT tokens.

**Request:**

.. code-block:: http

   POST /auth/login HTTP/1.1
   Content-Type: application/json

   {
     "email": "john@example.com",
     "password": "SecurePass123"
   }

**Response (200 OK):**

.. code-block:: json

   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": 1,
       "name": "John Doe",
       "email": "john@example.com",
       "user_type": "manager"
     }
   }

POST /auth/refresh
~~~~~~~~~~~~~~~~~~

Refresh an expired access token using a refresh token.

**Request:**

.. code-block:: http

   POST /auth/refresh HTTP/1.1
   Content-Type: application/json

   {
     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }

**Response (200 OK):**

.. code-block:: json

   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }

GET /auth/verify
~~~~~~~~~~~~~~~~

Verify if the current access token is valid.

**Authentication Required:** Yes

**Request:**

.. code-block:: http

   GET /auth/verify HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "message": "Token is valid",
     "user": {
       "id": 1,
       "email": "john@example.com",
       "user_type": "manager"
     }
   }

POST /auth/logout
~~~~~~~~~~~~~~~~~

Logout (client should discard tokens).

**Authentication Required:** Yes

**Request:**

.. code-block:: http

   POST /auth/logout HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "message": "Logged out successfully"
   }

User Management Endpoints
--------------------------

POST /users
~~~~~~~~~~~

Create a new user.

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   POST /users HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "name": "Jane Smith",
     "email": "jane@example.com",
     "password": "SecurePass456",
     "user_type": "employee"
   }

**Response (201 Created):**

.. code-block:: json

   {
     "id": 2,
     "name": "Jane Smith",
     "email": "jane@example.com",
     "user_type": "employee",
     "created_at": "2025-01-15T11:00:00Z",
     "updated_at": "2025-01-15T11:00:00Z"
   }

GET /users
~~~~~~~~~~

List all users with optional filtering.

**Authentication Required:** Yes

**Query Parameters:**

* ``user_type`` - Filter by "manager" or "employee"
* ``limit`` - Number of results (default: 50)
* ``offset`` - Pagination offset (default: 0)

**Request:**

.. code-block:: http

   GET /users?user_type=manager&limit=10 HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   [
     {
       "id": 1,
       "name": "John Doe",
       "email": "john@example.com",
       "user_type": "manager",
       "created_at": "2025-01-15T10:30:00Z",
       "updated_at": "2025-01-15T10:30:00Z"
     }
   ]

GET /users/<id>
~~~~~~~~~~~~~~~

Get a specific user by ID.

**Authentication Required:** Yes

**Query Parameters:**

* ``include_projects`` - Include user's projects (true/false)

**Request:**

.. code-block:: http

   GET /users/1?include_projects=true HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "id": 1,
     "name": "John Doe",
     "email": "john@example.com",
     "user_type": "manager",
     "created_at": "2025-01-15T10:30:00Z",
     "updated_at": "2025-01-15T10:30:00Z",
     "projects": [
       {
         "id": 1,
         "name": "Mobile App Development",
         "description": "Build a cross-platform app"
       }
     ]
   }

PUT /users/<id>
~~~~~~~~~~~~~~~

Update a user's information.

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   PUT /users/2 HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "name": "Jane Smith Updated",
     "user_type": "manager"
   }

**Response (200 OK):**

.. code-block:: json

   {
     "id": 2,
     "name": "Jane Smith Updated",
     "email": "jane@example.com",
     "user_type": "manager",
     "updated_at": "2025-01-15T12:00:00Z"
   }

DELETE /users/<id>
~~~~~~~~~~~~~~~~~~

Delete a user (cascades to projects and tasks).

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   DELETE /users/2 HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "message": "User deleted successfully"
   }

Project Management Endpoints
-----------------------------

POST /projects
~~~~~~~~~~~~~~

Create a new project.

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   POST /projects HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "name": "Mobile App Development",
     "description": "Build a cross-platform mobile application"
   }

**Response (201 Created):**

.. code-block:: json

   {
     "id": 1,
     "name": "Mobile App Development",
     "description": "Build a cross-platform mobile application",
     "user_id": 1,
     "created_at": "2025-01-15T10:35:00Z",
     "updated_at": "2025-01-15T10:35:00Z"
   }

GET /projects
~~~~~~~~~~~~~

List all projects with optional filtering.

**Authentication Required:** No

**Query Parameters:**

* ``user_id`` - Filter by project owner
* ``limit`` - Number of results
* ``offset`` - Pagination offset

**Request:**

.. code-block:: http

   GET /projects?user_id=1&limit=10 HTTP/1.1

**Response (200 OK):**

.. code-block:: json

   [
     {
       "id": 1,
       "name": "Mobile App Development",
       "description": "Build a cross-platform mobile application",
       "user_id": 1,
       "created_at": "2025-01-15T10:35:00Z",
       "updated_at": "2025-01-15T10:35:00Z"
     }
   ]

GET /projects/<id>
~~~~~~~~~~~~~~~~~~

Get a specific project by ID.

**Authentication Required:** No

**Query Parameters:**

* ``include_tasks`` - Include project's tasks (true/false)

**Request:**

.. code-block:: http

   GET /projects/1?include_tasks=true HTTP/1.1

**Response (200 OK):**

.. code-block:: json

   {
     "id": 1,
     "name": "Mobile App Development",
     "description": "Build a cross-platform mobile application",
     "user_id": 1,
     "created_at": "2025-01-15T10:35:00Z",
     "updated_at": "2025-01-15T10:35:00Z",
     "tasks": [
       {
         "id": 1,
         "title": "Design user interface",
         "description": "Create wireframes and mockups",
         "status": "pending"
       }
     ]
   }

PUT /projects/<id>
~~~~~~~~~~~~~~~~~~

Update a project's information.

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   PUT /projects/1 HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "name": "Mobile App Development - Updated",
     "description": "Updated description"
   }

**Response (200 OK):**

.. code-block:: json

   {
     "id": 1,
     "name": "Mobile App Development - Updated",
     "description": "Updated description",
     "user_id": 1,
     "updated_at": "2025-01-15T13:00:00Z"
   }

DELETE /projects/<id>
~~~~~~~~~~~~~~~~~~~~~

Delete a project (cascades to tasks).

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   DELETE /projects/1 HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "message": "Project deleted successfully"
   }

Task Management Endpoints
--------------------------

POST /projects/<project_id>/tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new task in a specific project.

**Authentication Required:** Yes
**Role Required:** Manager

**Request:**

.. code-block:: http

   POST /projects/1/tasks HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "title": "Design user interface",
     "description": "Create wireframes and mockups",
     "status": "pending"
   }

**Response (201 Created):**

.. code-block:: json

   {
     "id": 1,
     "title": "Design user interface",
     "description": "Create wireframes and mockups",
     "status": "pending",
     "project_id": 1,
     "created_at": "2025-01-15T10:40:00Z",
     "updated_at": "2025-01-15T10:40:00Z"
   }

GET /projects/<project_id>/tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get all tasks for a specific project.

**Authentication Required:** No

**Request:**

.. code-block:: http

   GET /projects/1/tasks HTTP/1.1

**Response (200 OK):**

.. code-block:: json

   [
     {
       "id": 1,
       "title": "Design user interface",
       "description": "Create wireframes and mockups",
       "status": "pending",
       "project_id": 1,
       "created_at": "2025-01-15T10:40:00Z",
       "updated_at": "2025-01-15T10:40:00Z"
     }
   ]

POST /tasks
~~~~~~~~~~~

Create a new task (alternative endpoint).

**Authentication Required:** Yes

**Request:**

.. code-block:: http

   POST /tasks HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "title": "Implement backend API",
     "description": "Create RESTful endpoints",
     "status": "in_progress",
     "project_id": 1
   }

**Response (201 Created):**

.. code-block:: json

   {
     "id": 2,
     "title": "Implement backend API",
     "description": "Create RESTful endpoints",
     "status": "in_progress",
     "project_id": 1,
     "created_at": "2025-01-15T11:00:00Z",
     "updated_at": "2025-01-15T11:00:00Z"
   }

GET /tasks
~~~~~~~~~~

Get all tasks with optional filtering.

**Authentication Required:** Yes

**Query Parameters:**

* ``status`` - Filter by "pending", "in_progress", or "completed"
* ``project_id`` - Filter by project
* ``limit`` - Number of results
* ``offset`` - Pagination offset

**Request:**

.. code-block:: http

   GET /tasks?status=in_progress&limit=10 HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   [
     {
       "id": 2,
       "title": "Implement backend API",
       "description": "Create RESTful endpoints",
       "status": "in_progress",
       "project_id": 1,
       "created_at": "2025-01-15T11:00:00Z",
       "updated_at": "2025-01-15T11:00:00Z"
     }
   ]

GET /tasks/<id>
~~~~~~~~~~~~~~~

Get a specific task by ID.

**Authentication Required:** No

**Request:**

.. code-block:: http

   GET /tasks/1 HTTP/1.1

**Response (200 OK):**

.. code-block:: json

   {
     "id": 1,
     "title": "Design user interface",
     "description": "Create wireframes and mockups",
     "status": "pending",
     "project_id": 1,
     "created_at": "2025-01-15T10:40:00Z",
     "updated_at": "2025-01-15T10:40:00Z"
   }

PUT /tasks/<id>
~~~~~~~~~~~~~~~

Update a task's information.

**Authentication Required:** Yes

**Request:**

.. code-block:: http

   PUT /tasks/1 HTTP/1.1
   Authorization: Bearer <access_token>
   Content-Type: application/json

   {
     "status": "in_progress",
     "description": "Updated description"
   }

**Response (200 OK):**

.. code-block:: json

   {
     "id": 1,
     "title": "Design user interface",
     "description": "Updated description",
     "status": "in_progress",
     "project_id": 1,
     "updated_at": "2025-01-15T14:00:00Z"
   }

DELETE /tasks/<id>
~~~~~~~~~~~~~~~~~~

Delete a task.

**Authentication Required:** Yes

**Request:**

.. code-block:: http

   DELETE /tasks/1 HTTP/1.1
   Authorization: Bearer <access_token>

**Response (200 OK):**

.. code-block:: json

   {
     "message": "Task deleted successfully"
   }

Common Error Responses
----------------------

Invalid Credentials
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Invalid email or password"
   }

**Status Code:** 401 Unauthorized

Unauthorized Access
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Authorization token is required"
   }

**Status Code:** 401 Unauthorized

Insufficient Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Manager role required"
   }

**Status Code:** 403 Forbidden

Resource Not Found
~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "User not found"
   }

**Status Code:** 404 Not Found

Validation Error
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "error": "Email is required"
   }

**Status Code:** 400 Bad Request

Best Practices
--------------

1. **Always use HTTPS in production** to protect tokens in transit
2. **Store tokens securely** on the client side (e.g., secure cookies, encrypted storage)
3. **Implement token refresh** before access tokens expire
4. **Use pagination** for list endpoints to manage large datasets
5. **Handle errors gracefully** and check status codes
6. **Include meaningful descriptions** when creating resources
7. **Use appropriate HTTP methods** (GET for reads, POST for creates, etc.)
8. **Validate input** on the client side before sending requests

Next Steps
----------

* Learn about :doc:`authentication` and JWT token management
* Review :doc:`design_rationale` for architectural decisions
* Explore the :doc:`modules` for code-level documentation
* Import the Postman collection for interactive API testing
