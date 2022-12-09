from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField(validators=[])
    password = PasswordField(validators=[])
    loginSubmit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(validators=[Length(min=4, message="Login musi zawierać co najmniej 4 znaki")])
    password = PasswordField(validators=[Length(min=6, message="Hasło musi zawierać co najmniej 6 znaków"),
                                         EqualTo('confirmPassword', message="Hasła muszą być identyczne")])
    confirmPassword = PasswordField(validators=[])
    email = EmailField(validators=[Email(message="Niepoprawny adres email")])
    registerSubmit = SubmitField()

