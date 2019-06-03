from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt, PUB_KEY
from flaskblog.models import User
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPassForm, PassForm
from flaskblog.users.utils import send_email, generate_confirmation_token, confirm_token
from flaskblog.main.forms import EmailForm
from flaskblog.main.utils import SendErrMail
import stripe
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = RegistrationForm()
        if form.validate_on_submit():

            cus = stripe.Customer.create(
                email=form.email.data.lower()

            )

            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user = User(name=form.name.data, email=form.email.data.lower(), password=hashed_password, customer_id=cus.id)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('users.confirm_email', token=token, _external=True)
            html = render_template("activate.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)

            login_user(user)

            flash('Your account has been created! A confirmation email has been sent.', 'success')
            return redirect(url_for('users.account'))
        return render_template("register.html", title="Register", form=form)
    except Exception as e:
        SendErrMail(e)

@users.route("/login", methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful', 'success')
                try:
                    website = User.query.filter_by(id=current_user.id).first()
                    return redirect(url_for('posts.post', domain=website.domain))
                except:
                    return redirect(url_for('users.account'))
            else:
                flash("Login Unsuccessful.", "danger")
        return render_template("login.html", title="Log In", form=form)
    except Exception as e:
        SendErrMail(e)

@users.route("/logout")
def logout():
    try:
        logout_user()
        flash('Logout successful!', 'success')
        return redirect(url_for('main.home'))
    except Exception as e:
        SendErrMail(e)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    try:
        form = EmailForm()
        if form.validate_on_submit():
            email = form.email_acc.data
            phone = form.phone.data
            content = form.content.data
            html = render_template("contacted.html", email=email, phone=phone, content=content)
            subject = email + " has contacted you"
            send_email('noreply@redlands.business', subject, html)
            flash("Successfully Contacted", 'success')
            return redirect(url_for('users.account'))
        return render_template("account.html", form=form, key=PUB_KEY)
    except Exception as e:
        SendErrMail(e)


@users.route('/account/update', methods=['GET', 'POST'])
@login_required
def account_update():
    try:
        form = UpdateAccountForm()
        website = User.query.filter_by(id=current_user.id).first()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.email = form.email.data.lower()
            cu = stripe.Customer.retrieve(current_user.customer_id)
            cu.email = current_user.email
            cu.save()
            db.session.commit()
            flash("Your account information has been updated!", 'success')
            return redirect(url_for('users.account'))
        elif request.method == 'GET':
            form.name.data = current_user.name
            form.email.data = current_user.email
        return render_template("update_account.html", title="Update Account Info", form=form, post=website)
    except Exception as e:
        SendErrMail(e)

@users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
            return redirect(url_for('users.login'))
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account. Thanks! Please create a website', 'success')
            return redirect(url_for('users.account'))
        return redirect(url_for('main.home'))
    except Exception as e:
        SendErrMail(e)

@users.route('/resend')
@login_required
def resend_confirmation():
    try:
        if not current_user.confirmed:
            token = generate_confirmation_token(current_user.email)
            confirm_url = url_for('users.confirm_email', token=token, _external=True)
            html = render_template("activate.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(current_user.email, subject, html)
            flash('Your account has been created! A confirmation email has been sent.', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Your account is already confirmed.', 'success')
            return redirect(url_for('users.account'))
    except Exception as e:
        SendErrMail(e)

@users.route("/password/forgot", methods=['GET', 'POST'])
def forgotpass():
    try:
        form = ResetPassForm()
        if form.validate_on_submit():
            email = form.email.data.lower()
            user = User.query.filter_by(email=email).first_or_404()
            if user:
                token = generate_confirmation_token(email)
                confirm_url = url_for('users.resetpass', token=token, _external=True)
                html = render_template("pass-reset-email.html", confirm_url=confirm_url)
                subject = "Your Password Reset Link"
                send_email(email, subject, html)
                flash('An email has been sent to reset your password.', 'success')
                return redirect(url_for('users.login'))
        return render_template("pass-forgot.html", form=form, title="Password Reset")
    except Exception as e:
        SendErrMail(e)

@users.route("/password/reset/<token>", methods=['GET', 'POST'])
def resetpass(token):
    try:
        form = PassForm()
        if form.validate_on_submit():
            try:
                email = confirm_token(token)
            except:
                flash('The link is invalid or has expired.', 'danger')
            user = User.query.filter_by(email=email).first_or_404()
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user.password = hashed_password
            db.session.commit()
            login_user(user)
            flash("Your password has been updated!", 'success')
            return redirect(url_for('users.account'))
        return render_template("pass-reset.html", form=form, title="Password Reset")
    except Exception as e:
        SendErrMail(e)

