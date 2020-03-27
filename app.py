"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "YOU WILLNVERFIGUREITOUT MUAHASLNALDKFNA"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home_page():
  """ redirects to users """

  return redirect("/users")

@app.route("/users")
def list_users():
  """ list users and show a button to add a user"""

  users = User.query.all()
  return render_template("userlist.html", users = users)

@app.route("/users/new")
def new_user_form():
  """ renders the new user form page"""

  return render_template("newuser.html")

@app.route("/users/new", methods =["POST"])
def add_user():
  """Add user and redirect to list."""

  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url']

  user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(user)
  db.session.commit()

  return redirect("/users")

@app.route("/users/<int:user_id>")
def show_userdetail(user_id):
  """show details about user """

  user = User.query.get_or_404(user_id)
  return render_template("userdetail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_user_edit_form(user_id):
  """show form to edit user details"""

  user = User.query.get_or_404(user_id)
  return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
  """Commits user edits to db and redirects to list."""
  
  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']

  db.session.commit()

  return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
  """Delete user form the db"""

  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  return redirect("/users")



##########################################################################

@app.route('/users/<int:user_id>/posts/new')
def show_newpost(user_id):
  """ Show form to add a post for that user"""

  user = User.query.get_or_404(user_id)
  tags = Tag.query.all()

  return render_template("newpost.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new',methods = ["POST"])
def add_post(user_id):
  """handle add form; add post and redirect to the user details"""

  user = User.query.get_or_404(user_id)
  content = request.form['content']
  new_post = Post(title=request.form['title'],
                  content=request.form['content'], user_id=user_id)

  db.session.add(new_post)
  db.session.commit()

  return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  """show a post and buttons to edit and delete the post"""

  post = Post.query.get_or_404(post_id)

  return render_template("postdetail.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
  """Show post edit page."""

  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()

  return render_template("postedit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
  """Accept edit to post and commit to db. Redirect to user page"""

  post = Post.query.get_or_404(post_id)

  post.title = request.form['title']
  post.content = request.form['content']

  db.session.commit()

  return redirect(f"/users/{post.user.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
  """Delete post from the db"""

  post = Post.query.get_or_404(post_id)
  user_id=post.user.id

  db.session.delete(post)
  db.session.commit()

  return redirect(f"/users/{user_id}")

@app.route("/tags")
def list_tags():

  tags = Tag.query.all()

  return render_template("tagslist.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):

  tag = Tag.query.get_or_404(tag_id)

  return render_template("tagdetail.html", tag=tag)

@app.route('/tags/new')
def show_newtag():
  """ Show form to add a post for that user"""


  return render_template("newtag.html")

@app.route('/tags/new',methods = ["POST"])
def add_tag():
  """handle add tag form; add tag and redirect to the tags list"""

  new_tag = Tag(name=request.form["name"])


  db.session.add(new_tag)
  db.session.commit()

  return redirect(f"/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
  """Show the edit page for the given tag"""

  tag = Tag.query.get_or_404(tag_id)

  return render_template("tagedit.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
  """Accept edit to tag and commit to db. Redirect to tag form"""

  tag = Tag.query.get_or_404(tag_id)

  tag.name = request.form['name']

  db.session.commit()

  return redirect(f"/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
  """Delete tag from the db"""

  tag = Tag.query.get_or_404(tag_id)


  db.session.delete(tag)
  db.session.commit()

  return redirect(f"/tags")