from flask import Blueprint

# Define a Blueprint for this module (mchat)
irsystem = Blueprint('irsystem', __name__, url_prefix='/',static_folder='static',template_folder='templates')

# Import all controllers
from controllers.query_response_controller import getQuery
from controllers.search_controller import *
