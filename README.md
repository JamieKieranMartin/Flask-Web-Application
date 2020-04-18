# Flask Web Application
Developed Dec 2017 - A Flask WebApp for creating and managing a web page for small businesses 

As a learning project I set out to build a CRUD web application utilising Flask, a micro web framework built on Python. This web application allows users to generate a single page website for their business under the domain name redlands.business. 

This project incorporates user authentication, token email certification, a database system, and Stripe integration (for charging higher tier users subscribed to certain website additions). These additions, which display on the users business page, include being able to capture emails for a newsletter, create an image gallery and to receive emails through a contact form on the businesses page. This is all handled by the web server, with no administrative input needed.

This project was built is hosted on PythonAnywhere, and utilises API libraries such as SQLAlchemy, WT-forms, and many more. By developing this project, my eyes were opened as to how professional websites are developed. I also gained interest for more complex website development.

Essentially users, can: register an account; login to said account; generate a business web page, and then manage it. Other endpoints were added for functionality ranging from forget password email authentication, error and payment emails to the domain owner.

- Once registered, and then logged in for the first time, the users will be required to authenticate via email token.
- Users must authenticate via email to generate a page. 
- Then users are able to fill out a form about their business with all necessary information. 
- Flask will generate a page for them using jinja2 (for python-html templating).
- The user can then manage and add features to the page from a dashboard. 
- Charges will automatically be added on to a monthly bill for specific addons using the Stripe API.
- Forget password and other error routes were implemented and revolve around email authentication as well.

All images, emails and keys have been hashed out or removed.
