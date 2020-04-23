from bookFlask import create_app, db
from bookFlask.auth.models import User

# app = create_app()

flask_app = create_app('dev')
# spin up the database and tables/models from the current app above
with flask_app.app_context():

    db.create_all()

    # this code says, if user_name 'harry' does not exist in our database
    # create that user
    # try:
    #     if not User.query.filter_by(user_name='harry').first():
    #         User.create_user(user='harry', email='harry@potters.com', password='secret')
    # except exc.IntegrityError:
    #     flask_app.run()

    if not User.query.filter_by(user_name='harry').first():
        User.create_user(user='harry', email='harry@potters.com', password='secret')

flask_app.run()