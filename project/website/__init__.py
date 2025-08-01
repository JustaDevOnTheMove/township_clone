from flask import Blueprint

files_blueprint = Blueprint('files', __name__, template_folder='templates')
pages_blueprint = Blueprint('pages', __name__, template_folder='templates')

from . import pages
from . import files
