from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from flask_mail import Message
from flaskblog.users.utils import send_email
from flaskblog import mail


def SendErrMail(err):
    if current_user.is_authenticated:
        html = render_template("error.html", user=current_user.email, error=str(err))
    else:
        html = render_template("error.html", user="Anonymous", error=str(err))
    subject = "Error Occured"
    send_email("**************", subject, html)
    string = "Error Occured" + str(err)
    flash(string, 'danger')
    return redirect(url_for('main.home'))