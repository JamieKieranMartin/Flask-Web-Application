from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class EmailForm(FlaskForm):
	email_acc = StringField('Email', validators=[DataRequired(), Email()])
	phone = StringField('Phone', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')