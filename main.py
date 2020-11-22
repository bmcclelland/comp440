from flask import Flask, request, session, render_template, redirect
import backend

app = Flask(__name__)

app.secret_key = b'123456789' # For session handling

def get_result_msg():
    result = request.args.get('result')
    if result is None:
        return ""
    elif result == 'bad_login':
        return 'Login failed: invalid username/password'
    elif result == 'name_in_use':
        return 'Registration failed: username already in use'
    elif result == 'email_in_use':
        return 'Registration failed: email already in use'
    elif result == 'initialized':
        return 'Database reinitialized'
    elif result == 'blogs_per_day':
        return 'Blog post failed: you cannot post more than 2 blogs per day'
    elif result == 'comments_per_day':
        return 'Comment failed: you cannot post more than 3 comments per day'
    elif result == 'comments_per_blog':
        return 'Comment failed: you cannot comment more than once per blog'
    elif result == 'comment_own_blog':
        return 'Comment failed: you cannot comment on your own blog'
    elif result == 'not_logged_in':
        return 'Error: you must be logged in to do that'
    else:
        raise Exception('unknown result: ' + str(result))

def get_username():
    return session.get('username')

def set_username(username):
    if username is None:
        session.pop('username', None)
    else:
        session['username'] = username

def std_template(t, **params):
    msg = get_result_msg()
    username = get_username()
    return render_template(t, msg=msg, username=username, **params)

@app.route('/')
def show_home():
    return show_bloglist()

@app.route('/')
def show_bloglist():
    blogs = backend.get_bloglist()
    return std_template('bloglist.html', blogs=blogs)

@app.route('/blog/<int:id>')
def show_blog(id):
    blog = backend.get_blog(id)
    if blog is None:
        return "Blog not found", 404
    else:
        return std_template('blog.html',blog=blog)

@app.route('/post')
def show_postblog():
    return std_template('postblog.html')

@app.route('/login')
def show_login():
    return std_template('login.html')

@app.route('/register')
def show_register():
    return std_template('register.html')

@app.route('/action/login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    if backend.verify_user(username, password):
        set_username(username)
        return redirect('/')
    else:
        set_username(None)
        return redirect('/login?result=bad_login')

@app.route('/action/register', methods=['POST'])
def action_register():
    username  = request.form['username']
    password  = request.form['password']
    email     = request.form['email']
    firstname = request.form['firstname']
    lastname  = request.form['lastname']

    if backend.verify_free_username(username):
        if backend.verify_free_email(email):
            backend.insert_user(username, password, email, firstname, lastname)
            return redirect('/')
        else:
            return redirect('/register?result=email_in_use')
    else:
        return redirect('/register?result=name_in_use')

@app.route('/action/initialize', methods=['POST'])
def action_initialize():
    backend.initialize();
    return redirect('/?result=initialized')

@app.route('/action/logout', methods=['GET'])
def action_logout():
    set_username(None)
    return redirect('/')

@app.route('/action/postblog', methods=['POST'])
def action_postblog():
    author = get_username()

    if author is None:
        return redirect('/post?result=not_logged_in')

    subject     = request.form['subject']
    description = request.form['description']
    tagsStr     = request.form['tags']
    tags = tagsStr.split(",")
    for tag in tags:
        tag = tag.strip()
    error = backend.create_blog(author, subject, description, tags)

    if error is None:
        return redirect('/')
    elif isinstance(error, backend.ErrorBlogsPerDay):
        return redirect('/post?result=blogs_per_day')

@app.route('/action/comment', methods=['POST'])
def action_comment():
    author = get_username()
    blogid = request.form['blogid']
    url = '/blog/' + str(blogid)

    if author is None:
        return redirect(url + '?result=not_logged_in')

    sentiment = request.form['sentiment']
    description = request.form['description']
    error = backend.create_comment(blogid, author, sentiment, description)

    if error is None:
        return redirect(url)
    elif isinstance(error, backend.ErrorCommentsPerDay):
        return redirect(url + '?result=comments_per_day')
    elif isinstance(error, backend.ErrorCommentsPerBlog):
        return redirect(url + '?result=comments_per_blog')
    elif isinstance(error, backend.ErrorCommentOwnBlog):
        return redirect(url + '?result=comment_own_blog')

if __name__ == '__main__':
    app.run()
