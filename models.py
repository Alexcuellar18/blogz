from app import db
from hashutils import make_pw_hash

class Blog(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  blog = db.Column(db.String(1200))
  owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))


  def __init__(self,title,blog,owner):
    self.title = title
    self.blog = blog
    self.owner = owner

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True)
  pw_hash = db.Column(db.String(120))
  blogs = db.relationship('Blog', backref='owner')

  def __init__(self,email,password):
    self.email = email
    self.pw_hash = make_pw_hash(password)
