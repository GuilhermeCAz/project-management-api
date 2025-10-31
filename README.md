# Project Management API

A robust and scalable RESTful API for project and task management, built with Flask and JWT authentication. This API provides complete user management, project organization, and task tracking capabilities with role-based access control.

## Features

- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **Role-Based Access Control** - Manager and Employee roles with different permissions
- **User Management** - Complete CRUD operations for user accounts
- **Project Management** - Create, organize, and manage projects
- **Task Management** - Track tasks within projects with status workflows
- **Input Validation** - Comprehensive validation for all endpoints
- **RESTful Design** - Clean, intuitive API following REST principles
- **Comprehensive Testing** - Full test coverage with pytest
- **API Documentation** - Sphinx-generated documentation
- **Structured Logging** - Enhanced logging with Loguru

## Technology Stack

- **Framework**: Flask 3.1.2
- **Database**: SQLAlchemy with SQLite (PostgreSQL-ready)
- **Authentication**: PyJWT 2.10.1 + bcrypt 5.0.0
- **Testing**: pytest + pytest-flask
- **Documentation**: Sphinx 8.2.3
- **Code Quality**: Ruff, mypy
- **Logging**: Loguru 0.7.3
- **Python**: 3.13+

## Quick Start

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd project-management-api
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. Run the application:

   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Overview

### Authentication Endpoints

| Method | Endpoint         | Description           | Auth Required |
| ------ | ---------------- | --------------------- | ------------- |
| POST   | `/auth/register` | Register a new user   | No            |
| POST   | `/auth/login`    | Login and get tokens  | No            |
| POST   | `/auth/refresh`  | Refresh access token  | No            |
| GET    | `/auth/verify`   | Verify token validity | Yes           |
| POST   | `/auth/logout`   | Logout confirmation   | Yes           |

### User Management

| Method | Endpoint      | Description     | Auth Required | Role Required |
| ------ | ------------- | --------------- | ------------- | ------------- |
| POST   | `/users`      | Create new user | Yes           | Manager       |
| GET    | `/users`      | List all users  | Yes           | -             |
| GET    | `/users/<id>` | Get user by ID  | Yes           | -             |
| PUT    | `/users/<id>` | Update user     | Yes           | Manager       |
| DELETE | `/users/<id>` | Delete user     | Yes           | Manager       |

### Project Management

| Method | Endpoint         | Description       | Auth Required | Role Required |
| ------ | ---------------- | ----------------- | ------------- | ------------- |
| POST   | `/projects`      | Create project    | Yes           | Manager       |
| GET    | `/projects`      | List all projects | No            | -             |
| GET    | `/projects/<id>` | Get project by ID | No            | -             |
| PUT    | `/projects/<id>` | Update project    | Yes           | Manager       |
| DELETE | `/projects/<id>` | Delete project    | Yes           | Manager       |

### Task Management

| Method | Endpoint                       | Description              | Auth Required | Role Required |
| ------ | ------------------------------ | ------------------------ | ------------- | ------------- |
| POST   | `/projects/<project_id>/tasks` | Create task in project   | Yes           | Manager       |
| GET    | `/projects/<project_id>/tasks` | Get all tasks in project | No            | -             |
| POST   | `/tasks`                       | Create task              | Yes           | -             |
| GET    | `/tasks`                       | Get all tasks            | Yes           | -             |
| GET    | `/tasks/<id>`                  | Get task by ID           | No            | -             |
| PUT    | `/tasks/<id>`                  | Update task              | Yes           | -             |
| DELETE | `/tasks/<id>`                  | Delete task              | Yes           | -             |

## Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "user_type": "manager"
  }'
```

Response:

```json
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
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Create a Project (Manager Only)

```bash
curl -X POST http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Mobile App Development",
    "description": "Build a cross-platform mobile application"
  }'
```

Response:

```json
{
  "id": 1,
  "name": "Mobile App Development",
  "description": "Build a cross-platform mobile application",
  "user_id": 1,
  "created_at": "2025-01-15T10:35:00Z",
  "updated_at": "2025-01-15T10:35:00Z"
}
```

### Create a Task

```bash
curl -X POST http://localhost:5000/projects/1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Design user interface",
    "description": "Create wireframes and mockups",
    "status": "pending"
  }'
```

Response:

```json
{
  "id": 1,
  "title": "Design user interface",
  "description": "Create wireframes and mockups",
  "status": "pending",
  "project_id": 1,
  "created_at": "2025-01-15T10:40:00Z",
  "updated_at": "2025-01-15T10:40:00Z"
}
```

### List Projects with Filtering and Pagination

```bash
# Get all projects by a specific user
curl "http://localhost:5000/projects?user_id=1&limit=10&offset=0"

# Get project with tasks included
curl "http://localhost:5000/projects/1?include_tasks=true"
```

### Update Task Status

```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "status": "in_progress"
  }'
```

## Database Models

### User

```python
{
  "id": int,
  "name": str,
  "email": str (unique),
  "password_hash": str,
  "user_type": "manager" | "employee",
  "created_at": datetime,
  "updated_at": datetime
}
```

### Project

```python
{
  "id": int,
  "name": str,
  "description": str (optional),
  "user_id": int (foreign key),
  "created_at": datetime,
  "updated_at": datetime
}
```

### Task

```python
{
  "id": int,
  "title": str,
  "description": str (optional),
  "status": "pending" | "in_progress" | "completed",
  "project_id": int (foreign key),
  "created_at": datetime,
  "updated_at": datetime
}
```

### Relationships

- **User → Projects**: One-to-Many (cascade delete)
- **Project → Tasks**: One-to-Many (cascade delete)

## Authentication & Authorization

### JWT Tokens

The API uses two types of JWT tokens:

- **Access Token**: Short-lived (1 hour), used for API requests
- **Refresh Token**: Long-lived (30 days), used to obtain new access tokens

### Token Payload

```json
{
  "user_id": 1,
  "email": "john@example.com",
  "user_type": "manager",
  "exp": 1234567890,
  "iat": 1234564290,
  "type": "access"
}
```

### Using Tokens

Include the access token in the Authorization header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Refreshing Tokens

```bash
curl -X POST http://localhost:5000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Role-Based Access Control

| Role         | Permissions                                                                       |
| ------------ | --------------------------------------------------------------------------------- |
| **Manager**  | Full access to all endpoints, can create/update/delete users, projects, and tasks |
| **Employee** | Can read users and projects, can create/update/delete tasks                       |

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///project_management.db

# Flask
FLASK_APP=run.py
FLASK_ENV=development

# Security
SECRET_KEY=your-secret-key-here

# Server
PORT=5000
```

### Configuration Classes

The application supports three environments:

- **Development** (`DevelopmentConfig`): Debug mode, SQLite database
- **Production** (`ProductionConfig`): No debug, configured for PostgreSQL
- **Testing** (`TestingConfig`): In-memory SQLite, testing mode

Set via `FLASK_ENV` environment variable.

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Available Fixtures

- `app` - Flask application instance
- `client` - Test client for API requests
- `manager_user` - Test manager user
- `employee_user` - Test employee user
- `auth_headers_manager` - Authorization headers for manager
- `auth_headers_employee` - Authorization headers for employee

## Documentation

### Generate Sphinx Documentation

```bash
cd docs
make html # On Windows: ./make.bat html
```

View documentation at `docs/_build/html/index.html`

### Available Documentation

- [Installation Guide](docs/installation.rst)
- [API Overview](docs/api_overview.rst)
- [Authentication Guide](docs/authentication.rst)
- [Module Reference](docs/modules.rst)

## Development

### Code Quality

The project uses strict code quality tools:

```bash
# Run linter
ruff check .

# Format code
ruff format .

# Type checking
mypy app
```

## API Testing with Postman

Import the included [postman_collection.json](postman_collection.json) file into Postman for a complete set of API requests with examples.

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Logging

The application uses Loguru for structured logging with color-coded output:

```python
from loguru import logger

logger.info("User logged in", user_id=user.id, email=user.email)
logger.error("Database error", error=str(e))
```

Logs include:

- Timestamp
- Log level (INFO, WARNING, ERROR)
- Module name
- Message
- Additional context

## Security Considerations

- Passwords are hashed using bcrypt with secure salts
- JWT tokens are signed with HS256 algorithm
- Access tokens expire after 1 hour
- SQL injection protection via SQLAlchemy ORM
- Input validation on all endpoints
- Cascade deletes prevent orphaned data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Run code quality checks (`ruff check . && mypy app`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
