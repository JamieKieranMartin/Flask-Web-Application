from flaskblog import db, login_manager
from flask_login import UserMixin
#from flask_security import Security, SQLAlchemyUserDatastore, \
 #   UserMixin, RoleMixin, login_required

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.Binary(60), nullable=False)
	confirmed = db.Column(db.Boolean, nullable=False, default=False)

	biz_name = db.Column(db.String(100), nullable=True)
	about = db.Column(db.Text, nullable=True)
	domain = db.Column(db.String(), nullable=True)
	no_ads = db.Column(db.Boolean, nullable=False, default = False)

	show_loc = db.Column(db.Boolean, nullable=False, default = False)
	address = db.Column(db.String(), nullable=True)
	address2 = db.Column(db.String(), nullable=True)
	city = db.Column(db.String(), nullable=True)
	state = db.Column(db.String(), nullable=True)
	post_code = db.Column(db.String(), nullable=True)
	logo_img = db.Column(db.String(), nullable=True)
	back_img = db.Column(db.String(), nullable=True)
	facebook = db.Column(db.String(), nullable=True)
	instagram = db.Column(db.String(), nullable=True)
	color_1 = db.Column(db.String(), nullable=True)
	color_2 = db.Column(db.String(), nullable=True)
	contact_email = db.Column(db.String(), nullable=True)
	contact_phone = db.Column(db.String(), nullable=True)
	abn = db.Column(db.String(11), nullable=True)

	custom_domain = db.Column(db.String(), nullable=True)
	custom_email = db.Column(db.String(), nullable=True)

	ecommerce = db.Column(db.Boolean(), nullable=False, default=False)

	bookings = db.Column(db.Boolean(), nullable=False, default=False)
	open = db.Column(db.String(), nullable=True)
	close = db.Column(db.String(), nullable=True)
	gallery = db.Column(db.Boolean(), nullable=False, default=False)
	newsletter = db.Column(db.Boolean(), nullable=False, default=False)
	contact_form = db.Column(db.Boolean(), nullable=False, default=False)

	customer_id = db.Column(db.String(), unique=True)
	subscription_id = db.Column(db.String())

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    img = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    datetime = db.Column(db.String(), nullable=False)
    info = db.Column(db.String(), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
