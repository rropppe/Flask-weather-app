from models import *


class RegistrationForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    email = StringField(validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField(validators={validators.DataRequired(),
                                         validators.EqualTo('confirm_password',
                                                            message='Пароли не совпадают')})
    confirm_password = PasswordField()


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField(validators=[validators.DataRequired()])