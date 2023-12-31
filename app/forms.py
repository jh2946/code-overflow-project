from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange
from app import ALLOWED_EXTENSIONS
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('',
                           validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('',
                        validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('',
                        validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    remember = BooleanField('')
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    photo = FileField('Upload photo here', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Invalid file extension'), FileRequired('File was empty!')])
    submit = SubmitField('Submit')

class ResultsForm(FlaskForm):
    quantity = FloatField('Quantity of food (g):', validators=[NumberRange(min=0, max=20000)])
    name = StringField('')
    info = StringField('')
    filename = StringField('')
