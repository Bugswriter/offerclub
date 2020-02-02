import secrets
import os
from flask_login import current_user
from flask import abort, current_app
from hungrynigga.models import User 
from PIL import Image



def adminCheck():
	if current_user.is_authenticated and current_user.username == 'bugswriter':
		pass
	else:
		abort(403)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/item_pics', picture_fn)

    output_size = (286, 180)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
