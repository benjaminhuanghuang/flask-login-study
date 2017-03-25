'''
Flask-Login-example (Login register facebook Login - Python Flask)
https://www.youtube.com/watch?v=5RlzqPz9oN8&feature=youtu.be&list=PLH4KIlK-M-evEMQwY5JQXwO-LiT-SR26E

https://github.com/twtrubiks/Flask-Login-example/
'''

import json
from functools import wraps

from flask import Flask, session, request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/vlc'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserAccount(db.Model):
    __tablename__ = 'user_accounts'

    Id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(64), unique=True)
    Password = db.Column(db.String(64))
    FBuserID = db.Column(db.String(32))
    FBAccessToken = db.Column(db.String(128))
    CreateDate = db.Column(db.DateTime)
    ModifiedDate = db.Column(db.DateTime)


class User(UserMixin):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')

    if request.method == 'GET':
        return render_template("login.html")

    if (current_user.is_authenticated and query_user(user_id)) or query_FBuser(user_id):
        return redirect(url_for('index'))

    username = request.form['username']
    user = UserAccount.query.filter_by(UserName=username).first()
    if user == None:
        return render_template("login.html", error="username or password error")
    pw_form = UserAccount.psw_to_md5(request.form['password'])
    pw_db = user.Password
    if pw_form == pw_db:
        user = User()
        user.id = username
        login_user(user, remember=True)
        flash('Logged in successfully')
        return redirect(url_for('index'))
    return render_template("login.html", error="username or password error")


def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_fun = func(*args, **kwargs)
        return json.dumps(get_fun)

    return wrapper


@app.route('/API_FB_login', methods=['POST'])
@to_json
def API_FB_login():
    userID = request.json['userID']
    accessToken = request.json['accessToken']
    FBuserID_Exist = UserAccount.query.filter_by(FBuserID=userID).first()
    if FBuserID_Exist == None:
        newAccount = UserAccount(UserName=None, Password=None, FBuserID=userID, FBAccessToken=accessToken)
        db.session.add(newAccount)
        user = User()
        user.id = userID
        login_user(user, remember=True)
    else:
        FBuserID_Exist.FBAccessToken = accessToken
        db.session.add(FBuserID_Exist)
        user = User()
        user.id = FBuserID_Exist.FBuserID
        login_user(user, remember=True)
    db.session.commit()
    return "11"


def query_user(username):
    user = UserAccount.query.filter_by(UserName=username).first()
    if user:
        return True
    return False


def query_FBuser(FBuserID):
    FBuser = UserAccount.query.filter_by(FBuserID=FBuserID).first()
    if FBuser:
        return True
    return False
