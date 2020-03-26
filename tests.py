from unittest import TestCase
from flask import session
from app import app
from models import User, Post

app.config['TESTING']=True
app.config['DEBUG_TB_HOSTS']=['DONT-SHOW-DEBUG-TOOLBAR']


class Blogly_Test_Cases(TestCase):
  """Testing the Blogly views"""

  def setUp(self):
    """Stuff to do before every test."""
    self.client = app.test_client()
    app.config['TESTING'] = True

  def test_new_user(self):
    with app.test_client() as client:
      resp = client.post('/users/new', data={'first_name': 'Test', 'last_name' : 'testers', 'image_url':'https://giphy.com/embed/l0Ex7SHlSIDcmYbBu'})
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 302)
    
  def test_new_user_to_user_list(self):
    with app.test_client() as client:
      resp = client.get('/users')
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn("Helen Seal", html)
