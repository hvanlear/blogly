from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///blogly"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

connect_db(app)


@app.route('/')
def root():
    """Homepage redirects to User List """

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)


@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/create_user.html')


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
    """show details about single user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show user edit form"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)


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
    flash(f'User {user.full_name} deleted')
    return redirect('/users')

######################## Posts Routes ###################################


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/create_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    # fix this redirect
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_content.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """"show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')

######################## Tag Routes ###################################


@app.route('/tags', methods=['GET'])
def show_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("tags.html", tags=tags)


@app.route('/tags/<int:tag_id>', methods=['GET'])
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


# @app.route('/tags/new')
# def show_tag_form
