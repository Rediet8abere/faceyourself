from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username',
                            validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('password',validators=[DataRequired()])
    confirmpassword = PasswordField('confirm password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')
