from flask_login import UserMixin
from app.extension import db,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(userID=user_id).first()


class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.userName

    def get_id(self):
        return self.userID