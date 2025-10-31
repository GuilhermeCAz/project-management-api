.. Project Management API documentation master file

Welcome to Project Management API Documentation
================================================

A robust and scalable RESTful API for project and task management, built with Flask and JWT authentication.

.. image:: https://img.shields.io/badge/Python-3.13+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/Flask-3.1.2-green.svg
   :target: https://flask.palletsprojects.com/
   :alt: Flask Version

Overview
--------

This API provides complete user management, project organization, and task tracking capabilities with role-based access control. It features:

* **JWT Authentication** - Secure token-based authentication with access and refresh tokens
* **Role-Based Access Control** - Manager and Employee roles with different permissions
* **User Management** - Complete CRUD operations for user accounts
* **Project Management** - Create, organize, and manage projects
* **Task Management** - Track tasks within projects with status workflows
* **Input Validation** - Comprehensive validation for all endpoints
* **RESTful Design** - Clean, intuitive API following REST principles

Quick Start
-----------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/GuilhermeCAz/project-management-api.git
   cd project-management-api

   # Install dependencies
   uv sync

   # Set up environment variables
   cp .env.example .env

   # Run the application
   python run.py

The API will be available at ``http://localhost:5000``

Technology Stack
----------------

* **Framework**: Flask 3.1.2
* **Database**: SQLAlchemy with SQLite (PostgreSQL-ready)
* **Authentication**: PyJWT 2.10.1 + bcrypt 5.0.0
* **Testing**: pytest + pytest-flask
* **Documentation**: Sphinx 8.2.3
* **Code Quality**: Ruff, mypy
* **Logging**: Loguru 0.7.3

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   authentication
   api_overview

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   design_rationale
   modules

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   contributing
   changelog

API Endpoints Summary
---------------------

Authentication
~~~~~~~~~~~~~~

* ``POST /auth/register`` - Register a new user
* ``POST /auth/login`` - Login and get tokens
* ``POST /auth/refresh`` - Refresh access token
* ``GET /auth/verify`` - Verify token validity
* ``POST /auth/logout`` - Logout confirmation

User Management
~~~~~~~~~~~~~~~

* ``POST /users`` - Create new user (Manager only)
* ``GET /users`` - List all users
* ``GET /users/<id>`` - Get user by ID
* ``PUT /users/<id>`` - Update user (Manager only)
* ``DELETE /users/<id>`` - Delete user (Manager only)

Project Management
~~~~~~~~~~~~~~~~~~

* ``POST /projects`` - Create project (Manager only)
* ``GET /projects`` - List all projects
* ``GET /projects/<id>`` - Get project by ID
* ``PUT /projects/<id>`` - Update project (Manager only)
* ``DELETE /projects/<id>`` - Delete project (Manager only)

Task Management
~~~~~~~~~~~~~~~

* ``POST /projects/<project_id>/tasks`` - Create task in project (Manager only)
* ``GET /projects/<project_id>/tasks`` - Get all tasks in project
* ``POST /tasks`` - Create task
* ``GET /tasks`` - Get all tasks
* ``GET /tasks/<id>`` - Get task by ID
* ``PUT /tasks/<id>`` - Update task
* ``DELETE /tasks/<id>`` - Delete task

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
