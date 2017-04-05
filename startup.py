#!/usr/bin/env python
"""Main Python script that starts the catalog app.
"""
import os.path

from catalog import app
from db.db_helper import create_db

if __name__ == '__main__':
    # App configuration
    app.config['DATABASE_URL'] = 'sqlite:///restaurantmenu.db'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)