from flask import Flask, request, render_template
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
app = Flask(__name__)
app.config['DEBUG'] = True

env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

basic_html = """
            <!doctype HTML>
            <html>
                <body>
                {0}
                </body>
            </html>

            """
login_form = """
            <form action="" method="POST">
                    <l>username:</l>
                    <input type="text" name="username" >
                    <l>Password:</l>
                    <input type="text" name="password1" >
                    <l>Confirm Password:</l>
                    <input type="text" name="password2" >
                    <l>E-Mail: (optional)</l>
                    <input type="text" name="email">
                    <input type="submit" value="Submit">
            </form>
            """
error_message = """
            <div>
                <p>Error! {0}</p>
            </div>
            """
@app.route("/")
def loginPage():
    template = env.get_template('login.html')
    #return basic_html.format(login_form)
    return template.render()
@app.route("/", methods=['POST'])
def attemptLogin():

    username_error = ''
    password_error1 = ''
    password_error2 = ''
    email_error = ''

    info = request.form
    template = env.get_template('login.html')
    # here we are checking to make sure the user input includes all required fields.
    
    if (info['username'] == ''):
        username_error="You are missing a username."
    if (info['password1'] == ''):    
        password_error1="You are missing your password."
    if (info['password2'] == ''): 
        password_error2="You are missing your password."


    if (" " in info['username']):
        username_error="Make sure there are no spaces in your username."
    if (" " in info['password1']):    
        password_error1="Make sure there are no spaces in your password."
    if (" " in info['password2']): 
        password_error2="Make sure there are no spaces in your password."
    if (" " in info['email']):
        email_error="Make sure there are no spaces in your email"
    # here we are making sure that the password confirmation matches. from here on we can
    # use validation for only password1 since we know that password1 and password2 match.
    if(not info['password1'] == info['password2']):
        password_error2='Your passwords do not match.'

    # username and password length validation
    if(len(info['username']) > 20):
        username_error="Your username is too long. Please make sure it is between 3 and 20 characters in length."
    if(len(info['username']) < 3):
        username_error="Your username is too short. Please make sure it is between 3 and 20 characters in length." 
    if(len(info['password1']) > 20):
        password_error1="Your password is too long. Please make sure it is between 3 and 20 characters in length."
    if(len(info['password1']) < 3):
        password_error1="Your password is too short. Please make sure it is between 3 and 20 characters in length." 

    # here we are making sure that the password confirmation matches. from here on we can
    # use validation for only password1 since we know that password1 and password2 match.
    if(not info['password1'] == info['password2']):
        password_error2='Your passwords do not match.'

    # email validation
    if not info['email'] == '':
        if (not info['email'].count('@') == 1) or (not info['email'].count('.') == 1):
            email_error="Your email is formatted invalidly." 
    if(len(username_error)==0 and len(password_error1)==0 and len(password_error2)==0 and len(email_error)==0):
        return render_template('index.html', username=info['username'])
    
    return template.render(username_error=username_error,password_error1=password_error1,password_error2=password_error2,
        email_error=email_error, username=info['username'],email=info['email'])

app.run()
