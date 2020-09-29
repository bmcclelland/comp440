from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def show_login():
    # show login form and register link
    # login form posts to action/login with parameters 'username' and 'password'
    return 'login or register'

@app.route('/action/login', methods=['POST'])
def action_login():
    # try logging in with username and password from request
    # if success, redirect to /loggedin
    # if error, redirect back to /
    return 'action/login'

@app.route('/loggedin')
def show_loggedin():
    # show page for when user is logged in
    return 'loggedin'

@app.route('/register')
def show_register():
    # show register form
    # form posts to action/register with parameters 'username' and 'password'
    return 'register'

@app.route('/action/register', methods=['POST'])
def action_register():
    # try registering with username and password from request
    # if success, redirect to /
    # if error, redirect back to /register
    return 'action/register'

if __name__ == '__main__':
    app.run()
