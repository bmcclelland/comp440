from flask import Flask, request, render_template, redirect
import backend

app = Flask(__name__)

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

@app.route('/')
def show_login():
    msg = get_result_msg()
    return render_template('index.html', msg=msg)

@app.route('/action/login', methods=['POST'])
def action_login():
    if backend.verify_user(request.form['username'], request.form['password']):
        return redirect('/loggedin')
    else:
        return redirect('/?result=bad_login')

@app.route('/loggedin')
def show_loggedin():
    return render_template('home.html')

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

if __name__ == '__main__':
    backend.create_user_table()
    app.run()
