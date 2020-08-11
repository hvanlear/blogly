from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    posts = db.relationship('Post')

    @property
    def full_name(self):
        """return full name of user"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

    @property
    def friendly_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


# user = User(first_name ='Hunter', last_name = 'VL')
# db.session.add(user)
# db.session


# users = [User(first_name = fn, last_name = ln) for fn,ln in zip(names, last_names)]
# users[0].first_name
# 'sushi'
# db.session.add_all(users)
# db.session.commit()


# post1.user.first_name
# post1.user.id
