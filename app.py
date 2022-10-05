from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email

#from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret.key"


@app.route('/')
def index():
    return render_template('index.html')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    loginSubmit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField([InputRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField()
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
        form.username.data, form.password.data, form.email.data = ''
    return render_template('register.html',
                           username=username,
                           password=password,
                           email=email,
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(e)
    return render_template('500.html', error=e), 500


if __name__ == '__main__':
    app.run()

