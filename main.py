from flask import Flask, request, redirect, render_template, session, flash
from hashutils import make_pw_hash,check_pw_hash
from app import app, db
from models import Blog,User 


@app.before_request
def require_login():
  allowed_routes = ['login', 'signup', 'index']
  if request.endpoint not in allowed_routes and'user' not in session:
    return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
  if request.method == 'GET':
      return render_template('login.html')
  elif request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      users = User.query.filter_by(email=email)
      if users.count() == 1:
          user = users.first()
          if user and check_pw_hash(password,user.pw_hash):
              session['user'] = user.email
              flash('welcome back, '+user.email)
              return redirect("/newpost")
      flash('bad username or password')
      return redirect("/login")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verified']
        if not is_email(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash('yikes! "' + email + '" is already taken.')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/newpost")
    else:
        return render_template('signup.html')

def is_email(string):

    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route('/', methods=['POST','GET'])
def index():
  user_id = request.args.get('user')

  if user_id:
    users = User.query.filter_by(id=user_id)
  else:
    users = User.query.all()

  return render_template('index.html', users=users, header='All Users')


@app.route('/blog', methods=['GET'])
def blog():
  
  blog_id = request.args.get('id')
  user_id = request.args.get('user')

  if blog_id:
    blogs = Blog.query.filter_by(id=blog_id).all()
    owner = User.query.filter_by(id= blogs[0].owner_id).first()
    return render_template('userblogs.html', blogs=blogs, user=owner)

  elif user_id:
    blogs = Blog.query.filter_by(owner_id = user_id)
    owner = User.query.filter_by(id=user_id).first()
    return render_template('userblogs.html', blogs=blogs, user=owner)
  else:
    blogs = Blog.query.all()
    users = User.query.all()
    return render_template('blog.html', blogs=blogs, users=users)
def empty_title(title):

  if len(title) > 1:
    return False
  else:
    return True

def empty_post(post):
  
  if len(post) > 1:
    return False
  else:
    return True


@app.route('/newpost', methods=['POST','GET'])
def newpost():
  blogs = Blog.query.all()

  owner = User.query.filter_by(email = session['user']).first()
  
  if request.method == 'POST':
    blog_title = request.form['blog_title']
    blog_post = request.form['blog_post']
    blog_entry = Blog(blog_title,blog_post,owner)
    if empty_title(blog_title) == True and empty_post(blog_post) == True:
      flash("You need to enter something! Both fields can not be blank",'error')
      return render_template('newpost.html', blog_entry=blog_entry)
    if empty_title(blog_title) == True:
      flash("The title of your post can not be empty.",'error')
      return render_template('newpost.html', blog_entry=blog_entry)
    elif empty_post(blog_post) == True:
      flash("Your blog post can not be empty.", 'error')
      return render_template('newpost.html', blog_title=blog_title)
    else:
      db.session.add(blog_entry)
      db.session.commit()
      blogs = Blog.query.filter_by(id=blog_entry.id).first()
    return redirect('/blog?id=' + str(blog_entry.id))
  else:
    return render_template('newpost.html')

@app.route('/logout', methods=['POST','GET'])
def logout():
  del session['user']
  return redirect('/login')



if __name__=='__main__':
  app.run()
  
