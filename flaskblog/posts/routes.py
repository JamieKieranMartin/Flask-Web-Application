from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db, PUB_KEY
from flaskblog.models import User, Images, Emails
from flaskblog.posts.forms import PostForm, UpdatePostForm, AddImageForm, AddEmailForm, CustomDomainForm, CustomEmailForm
from flaskblog.main.forms import EmailForm
from flaskblog.posts.utils import save_picture
from flaskblog.users.utils import send_email
from flaskblog.main.utils import SendErrMail
import stripe
import os

posts = Blueprint('posts', __name__)
@login_required
@posts.route("/new-website", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            website = User.query.filter_by(id=current_user.id).first()
            domain = str(form.biz_name.data).replace(" ", "-").lower()
            logo_img = None
            back_img = None
            if form.logo_img.data:
                logo_img = save_picture(form.logo_img.data)
            if form.back_img.data:
                back_img = save_picture(form.back_img.data)

            website.biz_name=form.biz_name.data
            website.about=form.about.data
            website.domain=domain
            website.show_loc = form.show_loc.data
            website.address=form.address.data
            website.address2=form.address2.data
            website.city=form.city.data
            website.state=form.state.data
            website.post_code=form.post_code.data
            website.logo_img=logo_img
            website.facebook=form.facebook.data
            website.instagram=form.instagram.data
            website.contact_email=form.contact_email.data
            website.contact_phone=form.contact_phone.data
            website.abn=form.abn.data
            website.back_img=back_img
            website.color_1=form.color_1.data
            website.color_2=form.color_2.data

            db.session.commit()
            string = "Your Website Has Been Created! Go to *************/" + str(form.biz_name.data).replace(" ", "-").lower() + " to see your website."
            flash(string, 'success')
            return redirect(url_for('posts.post', domain=domain))
        except Exception as e:
            SendErrMail(e)
    return render_template("create_website.html", title="New Website", form=form, legend="New Website")


@posts.route("/<string:domain>")
def post(domain):

    try:
        form = EmailForm()
        website = User.query.filter_by(domain=domain).first_or_404()
        if website is None:
            abort(404)
        newsletter = AddEmailForm()
        gallery = Images.query.filter_by(user=website.id).all()

    except Exception as e:
        SendErrMail(e)

    return render_template("post.html", website=website, gallery=gallery, key=PUB_KEY, form=form, newsletter=newsletter)


@posts.route("/<string:domain>/update", methods=['GET', 'POST'])
@login_required
def update_post(domain):
    try:
        website = User.query.filter_by(domain=domain).first()
        if website.id != current_user.id:
            abort(403)
        form = UpdatePostForm()
    except Exception as e:
        SendErrMail(e)
    if form.validate_on_submit():
        try:
            website = User.query.filter_by(domain=domain).first()
            logo_img = None
            back_img = None
            if form.logo_img.data != None:
                os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', website.logo_img))
                logo_img = save_picture(form.logo_img.data)
            if form.back_img.data != None:
                os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', website.back_img))
                back_img = save_picture(form.back_img.data)

            domain = str(form.biz_name.data).replace(" ", "-").lower()
            website.biz_name=form.biz_name.data
            website.about=form.about.data
            website.domain=domain
            website.show_loc = form.show_loc.data
            website.address=form.address.data
            website.address2=form.address2.data
            website.city=form.city.data
            website.state=form.state.data
            website.post_code=form.post_code.data
            website.logo_img=logo_img
            website.facebook=form.facebook.data
            website.instagram=form.instagram.data
            website.contact_email=form.contact_email.data
            website.contact_phone=form.contact_phone.data
            website.abn=form.abn.data
            website.back_img=back_img
            website.color_1=form.color_1.data
            website.color_2=form.color_2.data

            db.session.commit()
            flash("Your Website has been updated!", 'success')
            return redirect(url_for('posts.post', domain=website.domain))
        except Exception as e:
            SendErrMail(e)
    elif request.method == 'GET':
        try:
            form.biz_name.data = website.biz_name
            form.about.data = website.about
            domain = website.domain
            form.show_loc.data = website.show_loc
            form.address.data = website.address
            form.address2.data = website.address2
            form.city.data = website.city
            form.state.data = website.state
            form.post_code.data = website.post_code
            form.logo_img.data = website.logo_img
            form.facebook.data = website.facebook
            form.instagram.data = website.instagram
            form.contact_email.data = website.contact_email
            form.contact_phone.data = website.contact_phone
            form.abn.data = website.abn
            form.back_img.data = website.back_img
            form.color_1.data = website.color_1
            form.color_2.data = website.color_2

        except Exception as e:
            SendErrMail(e)

    return render_template("create_website.html", title="Update Website", form=form, legend="Update Website")

@posts.route("/<domain>/<plan_type>/charge", methods=['POST'])
@login_required
def charge(domain, plan_type, addon=None, addon2=None):
    website = User.query.filter_by(domain=domain).first()
    if website.id != current_user.id:
        abort(403)
    try:
        cus = stripe.Customer.retrieve(website.customer_id)
    except:
        cus = stripe.Customer.create(
                email=current_user.email,
            )
        current_user.customer_id = cus.id
    if not cus.sources:
        cus.source = request.form['stripeToken']
        cus.save()

    try:
        sub = stripe.Subscription.retrieve(current_user.subscription_id)
        stripe.SubscriptionItem.create(
            subscription=sub.id,
            plan=plan_type,
            quantity=1,
        )

    except:
        sub = stripe.Subscription.create(
            customer=cus.id,
            items=[
            {
              'plan':plan_type,
            },
            ])
        current_user.subscription_id = sub.id

    try:
        if plan_type == "***********":
            current_user.no_ads = True
            db.session.commit()
            html = render_template("purchase.html", user=current_user.email, purchase="Remove Advertisements")
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! Advertisements have been removed", 'success')
            return redirect(url_for('users.account'))
        elif plan_type == "***********":
            website.contact_form = True
            db.session.commit()
            html = render_template("purchase.html", user=current_user.email, purchase="Contact Form")
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! A contact form has been created on your site!", 'success')
            return redirect(url_for('users.account'))
        elif plan_type == "***********":
            website.gallery = True
            db.session.commit()
            html = render_template("purchase.html", user=current_user.email, purchase="Image Gallery")
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! An image gallery has been created on your site! Please add some images.", 'success')
            return redirect(url_for('users.account'))
        elif plan_type == "***********":
            website.newsletter = True
            db.session.commit()
            html = render_template("purchase.html", user=current_user.email, purchase="Newsletter")
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! An email form for newsletters has been created on your site!", 'success')
            return redirect(url_for('users.account'))
        elif plan_type == "***********":
            html = render_template("purchase.html", user=current_user.email, purchase=current_user.custom_domain)
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! Please allow 24 to 48 hours for your domain to propagate.", 'success')
            return redirect(url_for('posts.account'))
        elif plan_type == "***********":
            html = render_template("purchase.html", user=current_user.email, purchase=current_user.custom_email)
            subject = "A user has bought something"
            send_email("**************", subject, html)
            flash("Payment Successful! Please expect an email to discuss your email hosting.", 'success')
            return redirect(url_for('posts.account'))
    except Exception as e:
        SendErrMail(e)

@posts.route("/<domain>/domain/upgrade", methods=['GET', 'POST'])
@login_required
def upgrade(domain):
    try:
        website = User.query.filter_by(domain=domain).first()
        if website.id != current_user.id:
            abort(403)
        form = CustomDomainForm()
        if form.validate_on_submit():
            website.custom_domain = form.custom_domain.data
            db.session.commit()
            return redirect(url_for('posts.charge', domain=website.domain, plan_type="***********"), code=307)
        return render_template("create_paid_website.html", title="Upgrade Website", form=form, legend="Upgrade Website")
    except Exception as e:
        SendErrMail(e)


@posts.route("/<domain>/email/upgrade", methods=['GET', 'POST'])
@login_required
def upgrade_email(domain):
    try:
        website = User.query.filter_by(domain=domain).first()
        if website.id != current_user.id:
            abort(403)
        form = CustomEmailForm()
        if form.validate_on_submit():
            website.custom_email = form.custom_email.data
            db.session.commit()
            return redirect(url_for('posts.charge', domain=website.domain, plan_type="***********"), code=307)
        return render_template("upgrade_email.html", title="Add Email Hosting", form=form, legend="Add Email Hosting")
    except Exception as e:
        SendErrMail(e)


@posts.route("/<domain>/delete", methods=['POST'])
@login_required
def delete_post(domain):
    try:
        website = User.query.filter_by(domain=domain).first()
        if website.id != current_user.id:
            abort(403)
        images = Images.query.filter_by(user=website.id).all()

        os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', website.logo_img))
        os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', website.back_img))

        for image in images:
            os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', image.img))
            db.session.delete(image)

        website.about=None
        website.domain=None
        website.show_loc=True
        website.logo_img=None
        website.back_img=None
        website.facebook=None
        website.instagram=None
        website.color_1=None
        website.color_2=None

        db.session.commit()
        sub = stripe.Subscription.retrieve("*************")
        sub.delete()
        flash("Your Website has been deleted!", 'success')
        return redirect(url_for('users.account'))
    except Exception as e:
        SendErrMail(e)

@posts.route("/<domain>/contact-form/delete", methods=['POST'])
@login_required
def contact_form_delete(domain):
   website = User.query.filter_by(domain=domain).first()
   if website.id != current_user.id:
       abort(403)
   website.contact_form = False
   db.session.commit()
   flash("Your contact form has been removed from your site!", 'success')
   return redirect(url_for('users.account'))

@posts.route("/<domain>/contact_form_send", methods=['POST'])
def contact_form_send(domain):
    try:
        website = User.query.filter_by(domain=domain).first()
        form = EmailForm()
        if form.validate_on_submit():
            email = form.email_acc.data
            phone = form.phone.data
            content = form.content.data
            html = render_template("contacted.html", email=email, phone=phone, content=content)
            subject = email + " has contacted you on your website."
            send_email(website.contact_email, subject, html)
            flash("Successfully Contacted", 'success')
            return redirect(url_for('posts.post', domain=website.domain))
        return render_template("post.html", domain=website.domain)
    except Exception as e:
        SendErrMail(e)

@posts.route("/<domain>/image-gallery/delete", methods=['POST'])
@login_required
def image_gallery_delete(domain):
   website = User.query.filter_by(domain=domain).first()
   if website.id != current_user.id:
       abort(403)
   website.gallery = False
   images = Images.query.filter_by(user=current_user.id).all()
   for image in images:
       os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', image.img))
       db.session.delete(image)
   db.session.commit()
   flash("Your image gallery has been removed from your site!", 'success')
   return redirect(url_for('users.account'))

@posts.route("/<domain>/image/add", methods=['GET','POST'])
@login_required
def image_gallery_add(domain):
    try:
        form = AddImageForm()
        website = User.query.filter_by(domain=domain).first()
        if website.id != current_user.id:
            abort(403)
        if form.validate_on_submit():
            img = None
            if form.img.data:
                img = save_picture(form.img.data)
            title = form.title.data
            new_image = Images(title=title, img=img, user=current_user.id)
            db.session.add(new_image)
            db.session.commit()
            flash("Image added!", 'success')
            return redirect(url_for('users.account'))
        return render_template("image_add.html", form=form, title="Add Image", legend="Add Image")
    except Exception as e:
        SendErrMail(e)

@posts.route("/<domain>/<image_name>/delete", methods=['POST'])
@login_required
def image_delete(domain, image_name):
    try:
        website = User.query.filter_by(domain=domain).first_or_404()
        if website.id != current_user.id:
            abort(403)
        photo = Images.query.filter_by(id=image_name).one()
        os.remove(os.path.join('FlaskBlog/flaskblog/static/uploads', photo.img))
        db.session.delete(photo)
        db.session.commit()
        flash("Your image has been removed from your site!", 'success')
        return redirect(url_for('posts.post', domain=website.domain))
    except Exception as e:
        SendErrMail(e)


@posts.route("/<domain>/email/add", methods=['POST'])
def add_email_newsletter(domain):
    try:
        website = User.query.filter_by(domain=domain).first_or_404()
        newsletter = AddEmailForm()
        if newsletter.validate_on_submit():
            new_email = Emails(email=newsletter.email.data, user=website.id)
            db.session.add(new_email)
            db.session.commit()
            string = "Your email has been signed up for the " + website.biz_name +  " newsletter!"
            flash(string, 'success')
            return redirect(url_for('posts.post', domain=website.domain))
        return render_template("post.html", domain=website.domain)
    except Exception as e:
        SendErrMail(e)

