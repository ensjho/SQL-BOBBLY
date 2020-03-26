"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
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

  user = User(first_name = first_name, last_name = last_name, image_url = image_url)
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

  db.session.add(user) 
  "But we don't need this?"
  db.session.commit()

  return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
  """Delete user form the db"""

  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  return redirect("/users")



