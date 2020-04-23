from bookFlask import create_app, db
from bookFlask.auth.models import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask import Flask

flask_app = create_app('prod')
with flask_app.app_context():
    db.create_all()
    try:
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry', email='harry@potters.com', password='secret')
    except exc.IntegrityError:
        flask_app.run()