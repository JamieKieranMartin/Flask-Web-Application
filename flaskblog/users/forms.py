from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	name = StringField("Name",
						validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	password = PasswordField("Password",
						validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",
						validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Sign Up")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email is already taken")

class LoginForm(FlaskForm):
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	password = PasswordField("Password",
						validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
	name = StringField("Username",
						validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	submit = SubmitField("Update")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Email is already taken")

class ResetPassForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")

    def validate_an_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("No Email Exists")

class PassForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")