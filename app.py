from flask import Flask, render_template, url_for, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import Integer, String, Date, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret.key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/aiml'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Session(app)


@app.route('/')
def index():
    return render_template('index.html')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column('u_id', Integer, primary_key=True)
    username = db.Column('u_username', String, unique=True)
    email = db.Column('u_email', String, unique=True)
    password_hash = db.Column('u_password_hash', String)
    is_active = db.Column('u_active', Boolean, default=True)
    created = db.Column('u_created', Date, default=datetime.now())
    last_update = db.Column('u_last_update', Date)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, "sha256")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User(username='{}', email='{}', password_hash='{}', is_active='{}', created='{}', last_update='{}')" \
            .format(self.username, self.email, self.password_hash, self.is_active, self.created, self.last_update)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data, form.password.data = '', ''
        user = User.query.filter_by(username=username).first()
        if user:
            if not user.is_active:
                form.username.errors.append("Konto jest nieaktywne")
                return render_template('login.html', form=form)
            if check_password_hash(user.password_hash, password):
                login_user(user)
                session['id'] = user.get_id()
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                form.password.errors.append("Podano nieprawidłowe poświadczenia")
                return render_template('login.html', form=form)
        else:
            form.password.errors.append("Podano nieprawidłowe poświadczenia")
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session['id'] = None
    session['username'] = None
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    password = None
    email = None
    form = forms.RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if User.query.filter_by(email=email).first():
            form.email.errors.append("Podany adres email jest już w użyciu")
            return render_template('register.html', form=form)
        if User.query.filter_by(username=username).first():
            form.username.errors.append("Podana nazwa użytkownika jest już w użyciu")
            return render_template('register.html', form=form)
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        session['id'] = user.get_id()
        session['username'] = user.username
        return redirect(url_for('home'))
        form.password
        form.username.data, form.password.data, form.email.data, form.confirmPassword = '', '', '', ''
    return render_template('register.html',
                           username=username,
                           password=password,
                           email=email,
                           form=form)


@app.route('/home')
@login_required
def home():
    return render_template('home.html', session=session)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return render_template('404.html', error=e, error_code="404"), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(e)
    return render_template('500.html', error=e, error_code="500"), 500


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
