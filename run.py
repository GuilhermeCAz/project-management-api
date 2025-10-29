"""Application entry point.

Run this file to start the Flask development server.
"""

import os

from app import create_app

app = create_app()


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))

    app.run(host='localhost', port=port)
