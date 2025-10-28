# Impact Point - Backend Developer - Take-Home Assignment

## Task Overview

You are tasked with creating a robust and scalable backend API for a project management system using Flask. The API should allow users to manage projects and tasks, handling typical CRUD operations.

## Target Audience

The target audience is the Frontend developer that will utilize the information to build a scalable UI/UX.

## Requirements

### API Development

#### User Creation

Create endpoints for managing users:

- `POST /users`: Create a new user.
- `GET /users`: Retrieve a list of all users.
- `GET /users/<id>`: Retrieve a specific user by ID.
- `PUT /users/<id>`: Update an existing user.
- `DELETE /users/<id>`: Delete a user.
- There must be 2 user types: **manager** and **employee**.

#### Project Management

Create endpoints for managing projects:

- `POST /projects`: Create a new project.
- `GET /projects`: Retrieve a list of all projects.
- `GET /projects/<id>`: Retrieve a specific project by ID.
- `PUT /projects/<id>`: Update an existing project.
- `DELETE /projects/<id>`: Delete a project.

#### Task Management

Create endpoints for managing tasks within a project:

- `POST /projects/<id>/tasks`: Add a new task to a project.
- `GET /projects/<id>/tasks`: Retrieve all tasks for a specific project.

### Testing

- Create Unit Test for all functionality above using **Pytest**

### Validation & Error Handling

- Implement basic input validation and error handling to ensure the API is robust and user-friendly.
- Implement route guarding based on user type. Any route that affects the database should only be accessible to a **manager**.

### Database Design & Management

- Use **SQLAlchemy** to model your database.
- Design efficient data models for both projects and tasks, ensuring that relationships (e.g., a project has many tasks) are properly defined.
- Ensure that your database schema can handle a reasonable amount of data and queries efficiently.

### Documentation

#### Method Documentation

- Document every method/route you create using **Sphinx**

#### Setup Instructions

- Provide a **README.md** with clear instructions on how to set up and run the application locally.

#### Design Rationale

- Write a brief document explaining the choices behind your API design, database schema, and any optimizations implemented.

## Bonus Points

### Postman

- Share a Postman project with related documentation that we can use to test the endpoints.

### Extra Functionality

- Consider adding any extra functionality that might be useful in a real project management application.

## Submission

### GitHub Repository

- Share your GitHub repository link with your code.
- Ensure that it is **public**
- Ensure the repository includes all necessary code, configurations, tests, and documentation.

### Timeline

- Please submit your assignment within **7 days**.
