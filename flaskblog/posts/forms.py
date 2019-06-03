from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from flaskblog.models import User

class PostForm(FlaskForm):
	biz_name = StringField('Business Name', validators=[DataRequired()])
	about = TextAreaField('About', validators=[DataRequired()])
	show_loc = BooleanField('Show Street Address?')
	address = StringField("Street Address", validators=[DataRequired()])
	address2 = StringField("Street Address 2", validators=[Optional()])
	city = StringField("City", validators=[DataRequired()])
	state = SelectField("State", choices=[('ACT', 'ACT'), ('NSW', 'NSW'), ('NT', 'NT'), ('QLD', 'QLD'), ('SA', 'SA'), ('TAS', 'TAS'), ('VIC', 'VIC'), ('WA', 'WA')], validators=[DataRequired()])
	post_code = StringField("Post Code", validators=[DataRequired()])
	logo_img = FileField("Logo Image", validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
	back_img = FileField("Background Image", validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
	facebook = StringField("Facebook Account (Optional)", validators=[Optional()])
	instagram = StringField("Instagram Account (Optional)", validators=[Optional()])
	contact_email = StringField("Contact Email", validators=[DataRequired(), Email()])
	contact_phone = StringField("Contact Phone Number", validators=[DataRequired()])
	abn = StringField("ABN", validators=[Length(11), DataRequired()])
	color_1 = StringField("Text Colour", validators=[DataRequired()])
	color_2 = StringField("Background Colour", validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_abn(self, abn):
		abn = Post.query.filter_by(abn=abn.data).first()
		if abn:
		raise ValidationError("ABN already has a website attached to it.")

class UpdatePostForm(FlaskForm):
	biz_name = StringField('Business Name', validators=[DataRequired()])
	about = TextAreaField('About', validators=[DataRequired()])
	show_loc = BooleanField('Show Street Address?')
	address = StringField("Address", validators=[DataRequired()])
	address2 = StringField("Address 2", validators=[Optional()])
	city = StringField("City", validators=[DataRequired()])
	state = SelectField("State", choices=[('ACT', 'ACT'), ('NSW', 'NSW'), ('NT', 'NT'), ('QLD', 'QLD'), ('SA', 'SA'), ('TAS', 'TAS'), ('VIC', 'VIC'), ('WA', 'WA')], validators=[DataRequired()])
	post_code = StringField("Post Code", validators=[DataRequired()])
	logo_img = FileField("Logo Image", validators=[FileAllowed(['jpg', 'png'])])
	back_img = FileField("Background Image", validators=[FileAllowed(['jpg', 'png'])])
	facebook = StringField("Facebook Account (Optional)", validators=[Optional()])
	instagram = StringField("Instagram Account (Optional)", validators=[Optional()])
	contact_email = StringField("Contact Email", validators=[DataRequired(), Email()])
	contact_phone = StringField("Contact Phone Number", validators=[DataRequired()])
	abn = StringField("ABN", validators=[Length(11), DataRequired()])
	color_1 = StringField("Text Colour", validators=[DataRequired()])
	color_2 = StringField("Background Colour", validators=[DataRequired()])
	submit = SubmitField('Submit')

class CustomEmailForm(FlaskForm):
    custom_email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Submit')

class CustomDomainForm(FlaskForm):
    custom_domain = StringField("Domain Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddImageForm(FlaskForm):
    title = StringField('Title')
    img = FileField("Image", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class AddEmailForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Sign Up')