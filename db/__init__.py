"""Initialisation for the catalog package."""
from flask import Flask

# Initialise the Flask app object
app = Flask(__name__)

# Initialise SeaSurf anti-CSRF Flask extension


# Import modules that have the route() decorator in them.
# OK to have circular imports here as they are not used in this file.
# Ref: http://flask.pocoo.org/docs/0.10/patterns/packages/
import db.database_setup
import db.db_helper