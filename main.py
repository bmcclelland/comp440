from flask import Flask, request, render_template, redirect
import backend

app = Flask(__name__)

@app.route('/')
def show_login():
    return render_template('index.html')

@app.route('/action/login', methods=['POST'])
def action_login():
    if backend.verify_user(request.form['username'], request.form['password']):
        return redirect('/loggedin')
    else:
        # TODO error: invalid username/password
        return redirect('/')

@app.route('/loggedin')
def show_loggedin():
    return render_template('home.html')

@app.route('/register')
def show_register():
    return render_template('register.html')

@app.route('/action/register', methods=['POST'])
def action_register():
    if backend.retrieve_user(request.form['username']) is None:
        backend.insert_user(request.form['username'], request.form['password'])
        return redirect('/')
    else:
        # TODO error: username already exists
        return redirect('/register')

if __name__ == '__main__':
    backend.create_user_table()
    app.run()
