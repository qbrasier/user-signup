from flask import Flask, request
app = Flask(__name__)
app.config['DEBUG'] = True

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
                    <input type="text" name="username" required>
                    <l>Password:</l>
                    <input type="text" name="password1" required>
                    <l>Confirm Password:</l>
                    <input type="text" name="password2" required>
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

    return basic_html.format(login_form)
@app.route("/", methods=['POST'])
def attemptLogin():
    info = request.form

    # here we are checking to make sure the user input includes all required fields.
    # this is redundant because they are marked as required in the html form.
    if (info['username'] == ''):
        return basic_html.format(error_message.format("You are missing a username.") + login_form)
    if (info['password1'] == '') or (info['password2'] == ''):
        return basic_html.format(error_message.format("You need to fill out both password fields.") + login_form)     
    
    # here we are making sure that the password confirmation matches. from here on we can
    # use validation for only password1 since we know that password1 and password2 match.
    if(not info['password1'] == info['password2']):
        return  basic_html.format(error_message.format("Your passwords do not match.") + login_form) 

    # username and password length validation
    if(len(info['username']) > 20):
        return  basic_html.format(error_message.format("Your username is too long. Please make sure it is between 3 and 20 characters in length.") + login_form) 
    if(len(info['username']) < 3):
        return  basic_html.format(error_message.format("Your username is too short. Please make sure it is between 3 and 20 characters in length.") + login_form) 
    if(len(info['password1']) > 20):
        return  basic_html.format(error_message.format("Your password is too long. Please make sure it is between 3 and 20 characters in length.") + login_form) 
    if(len(info['password1']) < 3):
        return  basic_html.format(error_message.format("Your password is too short. Please make sure it is between 3 and 20 characters in length.") + login_form) 

    # email validation
    if not info['email'] == '':
        if (not info['email'].count('@') == 1) or (not info['email'].count('.') == 1):
            return basic_html.format(error_message.format("Your email is formatted invalidly.") + login_form) 

    return basic_html.format(login_form)


app.run()
