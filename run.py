"""Application entry point.

Run this file to start the Flask development server.
"""

import os

from app import create_app

app = create_app()


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    app.run(host='localhost', port=port, debug=debug)
