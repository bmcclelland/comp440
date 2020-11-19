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
    elif result == 'initialized':
        return 'Database reinitialized'
    else:
        raise Exception('unknown result: ' + str(result))

def get_username():
    return session.get('username')

def set_username(username):
    if username is None:
        session.pop('username', None)
    else:
        session['username'] = username

@app.route('/')
def show_home():
    msg = get_result_msg()
    username = get_username()
    if username is None:
        return render_template('index.html', msg=msg)
    else:
        return render_template('home.html', username=username)

@app.route('/')
def show_login():
    return show_home()

@app.route('/action/login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    if backend.verify_user(username, password):
        set_username(username)
        return redirect('/')
    else:
        set_username(None)
        return redirect('/?result=bad_login')

@app.route('/register')
def show_register():
    msg = get_result_msg()
    return render_template('register.html', msg=msg)

@app.route('/action/register', methods=['POST'])
def action_register():
    if backend.retrieve_user(request.form['username']) is None:
        backend.insert_user(request.form['username'], request.form['password'])
        return redirect('/')
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

if __name__ == '__main__':
    backend.create_user_table()
    app.run()
