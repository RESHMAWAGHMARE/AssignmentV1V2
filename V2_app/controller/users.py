from flask import Blueprint, request
from flask_dance.contrib.google import make_google_blueprint
import os
from config import app
from extension import logging
from app.service.g_login import google_login_check
from app.service.users import user_create

user = Blueprint('user', 'user')

google_login = make_google_blueprint(
    client_id=os.getenv('client_id_google'),
    client_secret=os.getenv('client_secret_google'),
    redirect_url="/google/callback",
    scope=["profile",
           "email",
           'https://www.googleapis.com/auth/calendar',
           'https://www.googleapis.com/auth/documents',
           'https://www.googleapis.com/auth/drive'
           ]
)

app.register_blueprint(google_login, url_prefix='/googlelogin')


@user.route('/google-login')
@user.route('/google/callback')
def google_login():
    logging.info(f"google-login:login successfully ")
    return google_login_check()


@user.route('/api/v1/users', methods=['POST'])
def create_user():
    logging.info("users-create_user function called.")
    return user_create(request.form)

