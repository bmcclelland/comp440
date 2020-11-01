from flask import Flask, request, render_template, redirect
import backend

app = Flask(__name__)

def get_error_msg():
    err = request.args.get('error')
    if err is None:
        return ""
    elif err == 'bad_login':
        return 'Login failed: invalid username/password'
    elif err == 'name_in_use':
        return 'Registration failed: username already in use'
    else:
        raise Exception('unknown error: ' + str(err))

@app.route('/')
def show_login():
    msg = get_error_msg()
    return render_template('index.html', msg=msg)

@app.route('/action/login', methods=['POST'])
def action_login():
    if backend.verify_user(request.form['username'], request.form['password']):
        return redirect('/loggedin')
    else:
        return redirect('/?error=bad_login')

@app.route('/loggedin')
def show_loggedin():
    return render_template('home.html')

@app.route('/register')
def show_register():
    msg = get_error_msg()
    return render_template('register.html', msg=msg)

@app.route('/action/register', methods=['POST'])
def action_register():
    if backend.retrieve_user(request.form['username']) is None:
        backend.insert_user(request.form['username'], request.form['password'])
        return redirect('/')
    else:
        return redirect('/register?error=name_in_use')

@app.route('/action/initialize', methods=['POST'])
def action_initialize():
    backend.initialize();
    return redirect('/')

if __name__ == '__main__':
    backend.create_user_table()
    app.run()
