import os
#import secrets
from PIL import Image
from flask import url_for
from flaskblog import app

def save_picture(form_picture):
    random_hex = os.urandom(24).encode('hex')
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path, optimize=True, quality=85)
    return picture_fn