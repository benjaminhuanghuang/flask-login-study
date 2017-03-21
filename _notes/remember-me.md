https://flask-login.readthedocs.io/en/latest/

By default, when the user closes their browser the Flask Session is deleted and the user is logged out. 
"Remember Me" prevents the user from accidentally being logged out when they close their browser. 
This does NOT mean remembering or pre-filling the user’s username or password in a login form after the 
user has logged out.

Flask-Login pass remember=True to the login_user call. A cookie will be saved on the user’s computer, 
and then Flask-Login will automatically restore the user ID from that cookie if it is not in the session. 
If the user tampers with it the cookie will merely be rejected, as if it was not there.

In the login view, if user login with "remember me" checked, we can find Flask will create a cookie "remember_token"
in the browser.
When user log out, Flask will delete it.

The settings of the "remember me"
    https://flask-login.readthedocs.io/en/latest/