from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask-login-study'
app.config['MONGO_DBNAME'] = 'flask-login-study'

mongo = PyMongo(app)

Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please tell me who are you.'


class User():
    def __init__(self, u):
        self.u = u
        self.username = u["user_name"]
        self.email = u["user_name"]
        self.password = u["password"]
        self.role = u.get("role", "user")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.u["_id"])


def validate_username_password(user_name, password):
    u = mongo.db['users'].find_one({"user_name": user_name})
    if not u or not check_password_hash(u["password"], password):
        return None
    return User(u)


def create_user(user_name, pwd):
    new_user = {
        "user_name": user_name,
        "password": generate_password_hash(pwd, method='pbkdf2:sha256')
    }
    _id = mongo.db['users'].insert(new_user)
    u = mongo.db['users'].find_one({"_id": _id})

    return User(u)


def is_user_existed(user_name):
    u = mongo.db['users'].find_one({"user_name": user_name})
    return u is not None


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db['users'].find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    user = User(u)
    return user


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Log In')

class RegisterForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = validate_username_password(form.username.data, form.password.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        if is_user_existed(user_name):
            flash('User name is existed.')
        else:
            user = create_user(user_name, password)
            login_user(user)
            return redirect(request.args.get('next') or url_for('dashboard'))

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
