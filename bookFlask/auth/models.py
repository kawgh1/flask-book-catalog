from datetime import datetime
from bookFlask import db, bcrypt # bookFlask/__init__.py
from bookFlask import login_manager

# UserMixin Class works with the database models
# UserMixin Class has attributes for users such as
#   'get_id', 'is_active', 'is_anonymous' and 'is_authenticated'
# all boolean values we can use to control access
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    # this takes the 'self' parameter because
    # this is an instance method we made and not a class method

    # meaning, this method doesn't get inheritted outside this file models.py file
    # it can only be called from another file
    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    # class methods belong to a class but are not associated with any class instance
    # ie. this method is belonging to the class User above, and not any particular instance of the class User

    @classmethod
    def create_user(cls, user, email, password):

        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8')
                   )

        db.session.add(user)
        db.session.commit()
        return user

# This is just an instance of the login_manager imported at top
@login_manager.user_loader
def load_user(id):
    # gets the UserID from the user table and returns the ID as an int
    # Flask-Login then stores the active user's ID in the session
    return User.query.get(int(id))