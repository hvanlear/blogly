from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        """return full name of user"""

        return f"{self.first_name} {self.last_name}"


# user = User(first_name ='Hunter', last_name = 'VL')
# db.session.add(user)
# db.session


# users = [User(first_name = fn, last_name = ln) for fn,ln in zip(names, last_names)]
# users[0].first_name
# 'sushi'
# db.session.add_all(users)
# db.session.commit()
