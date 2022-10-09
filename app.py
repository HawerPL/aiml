from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, String, Date, Boolean, MetaData
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret.key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/aiml'
db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template('index.html')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('u_id', Integer, primary_key=True)
    username = db.Column('u_username', String, unique=True)
    email = db.Column('u_email', String, unique=True)
    password_hash = db.Column('u_password_hash', String)
    is_active = db.Column('u_active', Boolean)
    created = db.Column('u_created', Date, default=datetime.now())
    last_update = db.Column('u_last_update', Date)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User(username='{}', email='{}', password_hash='{}', is_active='{}', created='{}', last_update='{}')"\
            .format(self.username, self.email, self.password_hash, self.is_active, self.created, self.last_update)


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    loginSubmit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), EqualTo('password', message="Hasła muszą być identyczne!")])
    confirmPassword = PasswordField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired(), Email()])
    registerSubmit = SubmitField()


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = None
    password = None
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data, form.password.data = '', ''
    return render_template('login.html',
                           username=username,
                           password=password,
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    password = None
    email = None
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if User.query.filter_by(email=email).first() is None or User.query.filter_by(username=username).first() is None:
            user = User(username=username, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
        form.username.data, form.password.data, form.email.data, form.confirmPassword = '', '', '', ''

    return render_template('register.html',
                           username=username,
                           password=password,
                           email=email,
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return render_template('404.html', error=e,  error_code="404"), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(e)
    return render_template('500.html', error=e, error_code="500"), 500


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()
