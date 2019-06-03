from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, Response
from flask_login import current_user, login_required
from flaskblog.models import User
from flaskblog.users.utils import send_email
from flaskblog.main.forms import EmailForm
from flaskblog.main.utils import SendErrMail

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def home():
    try:
        form = EmailForm()
        if form.validate_on_submit():
            email = form.email_acc.data
            phone = form.phone.data
            content = form.content.data
            html = render_template("contacted.html", email=email, phone=phone, content=content)
            subject = email + " has contacted you"
            send_email('**************', subject, html)
            flash("Successfully Contacted", 'success')
            return redirect(url_for('main.home'))
        return render_template('home.html', form=form)
    except Exception as e:
        SendErrMail(e)

@main.route("/privacy-policy", methods=['GET', 'POST'])
def privacy():
    try:
        form = EmailForm()
        if form.validate_on_submit():
            email = form.email_acc.data
            phone = form.phone.data
            content = form.content.data
            html = render_template("contacted.html", email=email, phone=phone, content=content)
            subject = email + " has contacted you"
            send_email('**************', subject, html)
            flash("Successfully Contacted", 'success')
            return redirect(url_for('main.home'))
        return render_template('privacy-policy.html', form=form)
    except Exception as e:
        SendErrMail(e)


