"""Blogly application."""

from flask import Flask
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

@app.route("/"):
def list_users():
    """ list users and show a button to add a user"""

  users = User.query.all()
  return render_template("userlist.html", users = users)

@app.route("/newuser", methods =["POST"])
def add_user():
  """Add user and redirect to list."""

  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url']

  user = User(first_name = first_name, last_name = last_name, image_url = image_url)
  db.session.add(user)
  db.session.commit()

  return redirect("/userlist")

@app.route("/userdetail/<int:user_id>"):
def show_userdetail():
  """show details about user """

  user = User.query.get_or_404(user_id)
  return render_template("userdetail.html", user=user)

