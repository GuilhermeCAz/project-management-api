# Documentation

This directory contains the Sphinx documentation for the Project Management API.

## Building the Documentation

### Prerequisites

Make sure you have Sphinx installed:

```bash
pip install sphinx sphinx-rtd-theme
# or if using uv
uv pip install sphinx sphinx-rtd-theme
```

### Linux/macOS

```bash
cd docs
make html
```

To view the documentation:

```bash
make view
```

To clean the build:

```bash
make clean
```

### Windows

```bash
cd docs
make.bat html
```

To view the documentation:

```bash
make.bat view
```

To clean the build:

```bash
make.bat clean
```

### Alternative (Cross-platform)

You can also use sphinx-build directly:

```bash
cd docs
sphinx-build -M html . _build
```

## Viewing the Documentation

After building, open the file `docs/_build/html/index.html` in your web browser.

**Linux/macOS:**

```bash
open _build/html/index.html
# or
xdg-open _build/html/index.html
```

**Windows:**

```bash
start _build\html\index.html
```

## Documentation Structure

```text
docs/
|-- conf.py                 # Sphinx configuration
|-- index.rst              # Main documentation index
|-- installation.rst       # Installation guide
|-- api_overview.rst       # API endpoints reference
|-- authentication.rst     # Authentication guide
|-- design_rationale.rst   # Design decisions
|-- modules.rst            # Auto-generated API reference
|-- contributing.rst       # Contributing guide
|-- changelog.rst          # Version history
|-- Makefile              # Build script for Linux/macOS
|-- make.bat              # Build script for Windows
|-- _static/              # Static files (CSS, images)
|-- _templates/           # Custom templates
`-- _build/               # Generated documentation (ignored by git)
```

## Documentation Pages

- **Installation**: Setup and configuration guide
- **API Overview**: Detailed endpoint documentation with examples
- **Authentication**: JWT authentication and authorization guide
- **Design Rationale**: Architectural decisions and trade-offs
- **API Reference**: Auto-generated from code docstrings
- **Contributing**: Guide for contributors
- **Changelog**: Version history and changes

## Live Reload (Optional)

For development, you can use sphinx-autobuild for live reload:

```bash
pip install sphinx-autobuild
cd docs
make livehtml  # Linux/macOS only
```

This will start a local server at <http://127.0.0.1:8000> that automatically rebuilds when you change files.

## Customization

### Theme

The documentation uses the Alabaster theme by default. To use the ReadTheDocs theme:

1. Install the theme:

   ```bash
   pip install sphinx-rtd-theme
   ```

2. Update `conf.py`:

   ```python
   html_theme = 'sphinx_rtd_theme'
   ```

### Adding New Pages

1. Create a new `.rst` file in the `docs/` directory
2. Add it to the `toctree` in `index.rst`:

   ```rst
   .. toctree::
      :maxdepth: 2

      installation
      your_new_page
   ```

## Troubleshooting

### Theme Not Found

If you see "no theme named 'sphinx_rtd_theme' found":

```bash
pip install sphinx-rtd-theme
```

Then update `conf.py` to use the theme.

### Module Import Errors

If Sphinx can't import your modules, check that:

1. The `sys.path.insert(0, os.path.abspath('..'))` is correct in `conf.py`
2. Your virtual environment is activated
3. The project is installed: `pip install -r requirements.txt`

### Build Warnings

Warnings about docstring formatting can usually be ignored, but fixing them improves documentation quality. Follow Google-style docstring format.

## Contributing to Documentation

When adding new features:

1. Update relevant `.rst` files
2. Add docstrings to your code
3. Rebuild documentation to verify
4. Commit both code and documentation changes

For detailed contribution guidelines, see [contributing.rst](contributing.rst).
