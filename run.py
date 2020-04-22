from bookFlask import create_app, db
from bookFlask.auth.models import User
from sqlalchemy import exc


# This is where we run the app. It is outside of the bookFlask folder
# by importing the create_app function, we can easily switch between 'dev', 'test' and 'prod'
# runtimes with a quick change here

# The next line was removed because it may not be relevant when we upload to webserver
# if __name__ == '__main__':

# 'flask_app' below is used in the Procfile
flask_app = create_app('prod')
# spin up the database and tables/models from the current app above
with flask_app.app_context():
    db.create_all()

    # this code says, if user_name 'harry' does not exist in our database
    # create that user
    try:
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@potters.com', password='secret')
    except exc.IntegrityError:
        flask_app.run()


# In order to upload to Heroku we need to install 'gunicorn' which is a Python HTTP server
#
# pip3 install gunicorn

# Then we have to create a 'requirements.txt' file - this is what Heroku looks for
#       to know what dependencies it needs to run our program/website
#
# command ==> 'pip freeze > requirements.txt'