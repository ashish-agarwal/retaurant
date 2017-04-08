#!/usr/bin/env python
"""Main Python script that starts the restaurant app.
"""
import os.path

from catalog import app

if __name__ == '__main__':
    # App configuration
    app.config['DATABASE_URL'] = 'sqlite:///restaurantmenu.db'
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
