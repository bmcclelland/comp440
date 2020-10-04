from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def show_login():
    return render_template('index.html')

@app.route('/action/login', methods=['POST'])
def action_login():
    # try logging in with username and password from request
    # if success, redirect to /loggedin
    # if error, redirect back to /
    return redirect('/loggedin')

@app.route('/loggedin')
def show_loggedin():
    return render_template('home.html')

@app.route('/register')
def show_register():
    return render_template('register.html')

@app.route('/action/register', methods=['POST'])
def action_register():
    # try registering with username and password from request
    # if success, redirect to /
    # if error, redirect back to /register
    return redirect('/')

if __name__ == '__main__':
    app.run()
