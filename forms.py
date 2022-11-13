from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    loginSubmit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), EqualTo('confirmPassword',
                                                                 message="Hasła muszą być identyczne!")])
    confirmPassword = PasswordField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired(), Email()])
    registerSubmit = SubmitField()

