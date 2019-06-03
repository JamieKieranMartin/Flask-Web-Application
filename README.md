# Flask Web Application
Developed Dec 2018 - A Web Application built on Flask which generates a web page for startup businesses. 

Built using flask_sqlalchemy, flask_bcrypt, flask_login, flask_mail, wtforms, jinja2 + the Stripe API.

Essentially users, can: register an account; login to said account; generate a business web page, and then manage it. Other endpoints were added for functionality ranging from forget password email authentication, error and payment emails to the domain owner.

- Once registered, and then logged in for the first time, the users will be required to authenticate via email token.
- Users must authenticate via email to generate a page. 
- Then users are able to fill out a form about their business with all necessary information. 
- Flask will generate a page for them using jinja2 (for python-html templating).
- The user can then manage and add features to the page from a dashboard. 
- Charges will automatically be added on to a monthly bill for specific addons using the Stripe API.
- Forget password and other error routes were implemented and revolve around email authentication as well.

