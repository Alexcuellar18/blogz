from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secretkey123'

class Blog(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  blog = db.Column(db.String(1200))

  def __init__(self,title,blog):
    self.title = title
    self.blog = blog

@app.route('/blog', methods=['GET'])
def index():

  blog_id =request.args.get('id')

  if blog_id:
    blogs = Blog.query.filter_by(id=blog_id)
  else:
    blogs = Blog.query.all()

  return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST','GET'])
def newpost():
  blogs = Blog.query.all()
  
  if request.method == 'POST':
    blog_title = request.form['blog_title']
    blog_post = request.form['blog_post']
    blog_entry = Blog(blog_title,blog_post)
    db.session.add(blog_entry)
    db.session.commit()
    blogs = Blog.query.filter_by(id=blog_entry.id).first()
    return redirect('/blog?id=' + str(blog_entry.id))
  else:
    return render_template('newpost.html')



if __name__=='__main__':
  app.run()
  
