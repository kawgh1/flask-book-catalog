# bookFlask/catalog/__init__.py


from flask import Blueprint


# Blueprint is a class

main = Blueprint('main', __name__, template_folder='templates')

from bookFlask.catalog import routes

