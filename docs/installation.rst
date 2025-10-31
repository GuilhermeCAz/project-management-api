Installation Guide
==================

This guide will help you set up the Project Management API on your local machine.

Requirements
------------

* Python 3.13 or higher
* pip or uv package manager
* Git

Installation Steps
------------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/GuilhermeCAz/project-management-api.git
   cd project-management-api

2. Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On Linux/macOS:**

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate

**On Windows:**

.. code-block:: bash

   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

**Using uv (recommended):**

.. code-block:: bash

   uv sync

**Using pip:**

.. code-block:: bash

   pip install -r requirements.txt

**For development (includes testing and linting tools):**

.. code-block:: bash

   uv sync --dev

4. Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file in the project root:

.. code-block:: bash

   cp .env.example .env

Edit the ``.env`` file and configure the following variables:

.. code-block:: bash

   # Database
   DATABASE_URL=sqlite:///project_management.db

   # Flask
   FLASK_APP=run.py
   FLASK_ENV=development

   # Security (REQUIRED - change this!)
   SECRET_KEY=your-secret-key-here

   # Server
   PORT=5000

.. important::
   Make sure to set a strong ``SECRET_KEY`` for JWT token signing. You can generate one using:

   .. code-block:: bash

      python -c "import secrets; print(secrets.token_hex(32))"

5. Initialize Database
~~~~~~~~~~~~~~~~~~~~~~

The database will be created automatically on the first run. If you want to initialize it manually:

.. code-block:: python

   from app import create_app, db

   app = create_app()
   with app.app_context():
       db.create_all()

6. Run the Application
~~~~~~~~~~~~~~~~~~~~~~

**Development server:**

.. code-block:: bash

   python run.py

**With custom port:**

.. code-block:: bash

   PORT=8000 python run.py

**Production with Gunicorn (Linux/macOS):**

.. code-block:: bash

   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

The API will be available at ``http://localhost:5000``

7. Verify Installation
~~~~~~~~~~~~~~~~~~~~~~~

Test the API is running:

.. code-block:: bash

   curl http://localhost:5000/auth/verify

You should receive a 401 error (expected, as you're not authenticated yet).

Configuration Options
---------------------

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default configuration for local development:

* Debug mode enabled
* SQLite database
* Verbose error messages

.. code-block:: bash

   export FLASK_ENV=development  # Linux/macOS
   set FLASK_ENV=development     # Windows

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Optimized for production deployment:

* Debug mode disabled
* PostgreSQL support
* Secure error handling

.. code-block:: bash

   export FLASK_ENV=production   # Linux/macOS
   set FLASK_ENV=production      # Windows

Testing Configuration
~~~~~~~~~~~~~~~~~~~~~

Used by the test suite:

* In-memory SQLite database
* Isolated test environment

.. code-block:: bash

   export FLASK_ENV=testing      # Linux/macOS
   set FLASK_ENV=testing         # Windows

Database Configuration
----------------------

SQLite (Default)
~~~~~~~~~~~~~~~~

No additional setup required. The database file will be created automatically.

.. code-block:: bash

   DATABASE_URL=sqlite:///project_management.db

PostgreSQL (Production)
~~~~~~~~~~~~~~~~~~~~~~~

Install PostgreSQL and create a database:

.. code-block:: bash

   # Create database
   createdb project_management

   # Set DATABASE_URL in .env
   DATABASE_URL=postgresql://user:password@localhost/project_management

Running Tests
-------------

Install development dependencies:

.. code-block:: bash

   uv sync --group dev

Run all tests:

.. code-block:: bash

   pytest

Run specific test file:

.. code-block:: bash

   pytest tests/test_auth.py

Code Quality Tools
------------------

Linting
~~~~~~~

Check code with Ruff:

.. code-block:: bash

   ruff check .

Format code:

.. code-block:: bash

   ruff format .

Type Checking
~~~~~~~~~~~~~

Run mypy for static type checking:

.. code-block:: bash

   mypy app

Building Documentation
----------------------

Install Sphinx (included in dev dependencies):

.. code-block:: bash

   cd docs

**On Linux/macOS:**

.. code-block:: bash

   make html

**On Windows:**

.. code-block:: bash

   make.bat html

View the documentation:

.. code-block:: bash

   # Linux/macOS
   open _build/html/index.html

   # Windows
   start _build\html\index.html

Troubleshooting
---------------

Port Already in Use
~~~~~~~~~~~~~~~~~~~

If port 5000 is already in use:

.. code-block:: bash

   PORT=8000 python run.py

Database Locked Error
~~~~~~~~~~~~~~~~~~~~~

SQLite database is locked (common in development):

.. code-block:: bash

   # Remove the database file and restart
   rm project_management.db
   python run.py

Import Errors
~~~~~~~~~~~~~

If you encounter import errors, make sure you're in the project root and have activated the virtual environment:

.. code-block:: bash

   # Activate virtual environment
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

   # Reinstall in editable mode
   uv sync

Permission Denied
~~~~~~~~~~~~~~~~~

On Linux/macOS, if you get permission errors:

.. code-block:: bash

   # Make run.py executable
   chmod +x run.py

   # Or run with python explicitly
   python run.py

Next Steps
----------

* Read the :doc:`authentication` guide to learn about JWT tokens
* Explore the :doc:`api_overview` for detailed endpoint documentation
* Check out :doc:`design_rationale` to understand architectural decisions
* Import the Postman collection for API testing
