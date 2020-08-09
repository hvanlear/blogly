from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///blogly"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

connect_db(app)


@app.route('/')
def root():
    """Homepage redirects to User List """
    return redirect('/users')


@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('create_user.html')


@app.route('/users/new', methods=["POST"])
def create_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_user = User(first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about single pet"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show user edit form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_update(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """ Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
