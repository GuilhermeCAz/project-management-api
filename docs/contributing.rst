Contributing Guide
==================

Thank you for considering contributing to the Project Management API! This guide will help you get started.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/GuilhermeCAz/project-management-api.git
      cd project-management-api

3. Create a virtual environment and install dependencies:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      uv sync --group dev


4. Create a branch for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

Development Workflow
--------------------

Code Style
~~~~~~~~~~

We use strict code quality tools to maintain consistency:

**Ruff** for linting and formatting:

.. code-block:: bash

   # Check code
   ruff check .

   # Format code
   ruff format .

   # Fix auto-fixable issues
   ruff check --fix .

**mypy** for type checking:

.. code-block:: bash

   mypy app

**Configuration**:

* Line length: 79 characters
* Quote style: Single quotes
* Strict type checking enabled

Running Tests
~~~~~~~~~~~~~

Always run tests before submitting changes:

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/test_auth.py

   # Run specific test
   pytest tests/test_auth.py::test_register_success

Writing Tests
~~~~~~~~~~~~~

Test files should mirror the app structure:

.. code-block:: text

   app/
   ├── auth/
   │   └── routes.py
   tests/
   └── test_auth.py

**Test Structure**:

.. code-block:: python

   import pytest
   from app import create_app, db

   def test_feature_name(client):
       """Test description.

       This test verifies that...
       """
       # Arrange
       data = {'key': 'value'}

       # Act
       response = client.post('/endpoint', json=data)

       # Assert
       assert response.status_code == 200
       assert response.get_json()['key'] == 'value'

**Use Fixtures**:

.. code-block:: python

   def test_authenticated_endpoint(client, auth_headers_manager):
       """Test with authentication."""
       response = client.get('/users', headers=auth_headers_manager)
       assert response.status_code == 200

Documentation
~~~~~~~~~~~~~

Update documentation for all changes:

**Code Documentation**:

* Use Google-style docstrings
* Document all public functions and classes
* Include parameter types and return types

.. code-block:: python

   def create_user(name: str, email: str) -> User:
       """Create a new user.

       Args:
           name: The user's full name
           email: The user's email address

       Returns:
           The newly created User object

       Raises:
           ValueError: If email is invalid
       """
       pass

**Sphinx Documentation**:

Update relevant ``.rst`` files in the ``docs/`` directory:

.. code-block:: bash

   cd docs
   make html  # Linux/macOS
   make.bat html  # Windows

Commit Messages
~~~~~~~~~~~~~~~

Write clear, descriptive commit messages:

**Format**:

.. code-block:: text

   type(scope): short description

   Longer explanation if needed.

   - Bullet points for details
   - Reference issues: Fixes #123

**Types**:

* ``feat``: New feature
* ``fix``: Bug fix
* ``docs``: Documentation changes
* ``style``: Code style changes (formatting)
* ``refactor``: Code refactoring
* ``test``: Test additions or changes
* ``chore``: Maintenance tasks

**Examples**:

.. code-block:: text

   feat(auth): add password reset functionality

   Implements password reset via email with secure tokens.

   - Add /auth/forgot-password endpoint
   - Add /auth/reset-password endpoint
   - Add email service integration
   - Add tests for new endpoints

   Fixes #45

.. code-block:: text

   fix(tasks): prevent duplicate task creation

   Add unique constraint on task title within projects.

   Fixes #67

Pull Request Process
--------------------

1. **Update your branch** with the latest main:

   .. code-block:: bash

      git checkout main
      git pull upstream main
      git checkout your-feature-branch
      git rebase main

2. **Run all quality checks**:

   .. code-block:: bash

      # Format code
      ruff format .

      # Run linter
      ruff check .

      # Type check
      mypy app

3. **Push to your fork**:

   .. code-block:: bash

      git push origin your-feature-branch

4. **Create Pull Request**:

   * Go to the repository on GitHub
   * Click "New Pull Request"
   * Select your branch
   * Fill out the template

Pull Request Template
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: markdown

   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] All tests pass
   - [ ] New tests added
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings

Review Process
~~~~~~~~~~~~~~

* At least one approval required
* All CI checks must pass
* Address all review comments
* Keep PR scope focused and small

What to Contribute
------------------

Good First Issues
~~~~~~~~~~~~~~~~~

Look for issues labeled ``good first issue``:

* Documentation improvements
* Bug fixes
* Minor feature enhancements

Feature Requests
~~~~~~~~~~~~~~~~

Before implementing a new feature:

1. Check existing issues
2. Create a feature request issue
3. Discuss the approach
4. Get approval before starting

Bug Reports
~~~~~~~~~~~

**Include**:

* Clear description
* Steps to reproduce
* Expected vs actual behavior
* Environment details (OS, Python version)
* Error messages/logs

**Template**:

.. code-block:: markdown

   ## Bug Description
   Brief description

   ## Steps to Reproduce
   1. Step one
   2. Step two
   3. ...

   ## Expected Behavior
   What should happen

   ## Actual Behavior
   What actually happens

   ## Environment
   - OS: Windows 11
   - Python: 3.13.0
   - Flask: 3.1.2

   ## Additional Context
   Any other relevant information

Code Review Guidelines
----------------------

For Reviewers
~~~~~~~~~~~~~

* Be respectful and constructive
* Explain reasoning for suggestions
* Distinguish between "must fix" and "nice to have"
* Approve if code is good enough (don't demand perfection)

For Contributors
~~~~~~~~~~~~~~~~

* Respond to all comments
* Ask questions if unclear
* Don't take feedback personally
* Make requested changes or discuss alternatives

Architecture Decisions
----------------------

For significant changes:

1. **Create an issue** describing the problem
2. **Propose a solution** with alternatives considered
3. **Discuss trade-offs** with maintainers
4. **Document the decision** in ``DESIGN_RATIONALE.md``
5. **Implement** after approval

Project Structure
-----------------

Understanding the codebase:

.. code-block:: text

   project-management-api/
   ├── app/
   │   ├── __init__.py           # App factory
   │   ├── auth/                 # Authentication
   │   │   ├── routes.py
   │   │   ├── services.py
   │   │   └── validators.py
   │   ├── users/                # User management
   │   ├── projects/             # Project management
   │   ├── tasks/                # Task management
   │   └── middleware/           # Auth middleware
   ├── tests/                    # Test suite
   ├── docs/                     # Sphinx docs
   ├── config.py                 # Configuration
   ├── run.py                    # Entry point
   └── pyproject.toml           # Dependencies

**Key Files**:

* ``app/__init__.py``: Application factory pattern
* ``config.py``: Environment configurations
* ``app/middleware/auth.py``: Authentication decorators
* ``tests/conftest.py``: Shared test fixtures

Adding New Features
-------------------

New Endpoint
~~~~~~~~~~~~

1. **Create route** in appropriate blueprint
2. **Add validation** in ``validators.py``
3. **Add tests** in corresponding test file
4. **Update documentation** in ``docs/api_overview.rst``
5. **Update Postman collection**

New Model
~~~~~~~~~

1. **Define model** in ``models.py``
2. **Add relationships** to related models
3. **Create migration** (if using Alembic)
4. **Add tests** for model validation
5. **Update documentation** in ``docs/``

Dependencies
------------

Adding Dependencies
~~~~~~~~~~~~~~~~~~~

Add to ``pyproject.toml`` under ``dependencies``:

.. code-block:: toml

   dependencies = [
       "flask>=3.1.2",
       "new-package>=1.0.0",
   ]

**Considerations**:

* Is it really needed?
* Is it maintained?
* What's the license?
* Does it add security risks?

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

Add under ``[project.optional-dependencies]``:

.. code-block:: toml

   [project.optional-dependencies]
   dev = [
       "pytest>=8.0.0",
       "new-dev-tool>=1.0.0",
   ]

Release Process
---------------

(For maintainers)

1. **Update version** in ``pyproject.toml``
2. **Update CHANGELOG.md**
3. **Run all tests**
4. **Build documentation**
5. **Create release tag**
6. **Push to GitHub**
7. **Create GitHub release**

Community
---------

* **Be respectful** of all contributors
* **Help others** when you can
* **Share knowledge** through documentation
* **Give credit** where it's due

Questions?
----------

* Check the :doc:`index` for general information
* Read :doc:`design_rationale` for architectural context
* Open an issue for discussion
* Reach out to maintainers

Thank you for contributing! 🎉
