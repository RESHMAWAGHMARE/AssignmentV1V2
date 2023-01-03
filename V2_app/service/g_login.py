from flask import redirect, url_for, jsonify, session
from flask_dance.contrib.google import google
import os
from datetime import datetime
import json
from app.models.user_query import insert_user, exist_user
from extension import logging

GOOGLE_LOGIN = "google.login"

session_folder = 'session'

credentials_data = {
    "web":
        {
            "client_id": os.getenv('client_id_google'),
            "project_id": os.getenv('project_id_google'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": os.getenv('client_secret_google'),
            "redirect_uris": ["http://localhost"],
            "javascript_origins": ["http://localhost"]
        }
}

if not os.path.exists(session_folder):
    os.mkdir(session_folder)

with open(f'{session_folder}/credentials.json', 'w') as file2:
    file2.write(json.dumps(credentials_data))


def google_login_check():
    try:
        if not google.authorized:
            response = redirect(url_for(GOOGLE_LOGIN))
        resp = google.get("oauth2/v2/userinfo")
        if resp.ok:
            resp = resp.json()
            user_info = {
                'user_id': resp['id'],
                'profile_url': resp['picture'],
                'name': resp['name'],
                'email': resp['email']
            }
            if not exist_user(user_info['user_id']):
                insert_user(user_info)
            session['current_user_id'] = user_info['user_id']
            response = jsonify(
                {
                    'status': 200,
                    'message': 'Login Successfully',
                    'user_id': user_info['user_id']
                }
            )
            google_oauth_token = session.get('google_oauth_token')

            if google_oauth_token:
                diff = datetime.fromtimestamp(google_oauth_token['expires_at']) - datetime.now()
                token_json = {
                    "access_token": google_oauth_token.get('access_token'),
                    "client_id": os.getenv('client_id_google'),
                    "client_secret": os.getenv('client_secret_google'),
                    "refresh_token": google_oauth_token.get('refresh_token'),
                    "token_expiry": f"{str(datetime.fromtimestamp(google_oauth_token['expires_at'])).replace(' ', 'T')}Z",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "user_agent": None,
                    "revoke_uri": "https://oauth2.googleapis.com/revoke",
                    "id_token": None,
                    "id_token_jwt": None,
                    "token_response": {
                        "access_token": google_oauth_token.get('access_token'),
                        "expires_in": diff.seconds,
                        "refresh_token": google_oauth_token.get('refresh_token'),
                        "scope": "https://www.googleapis.com/auth/calendar",
                        "token_type": "Bearer"
                    },
                    "scopes": ["https://www.googleapis.com/auth/calendar",
                       "https://www.googleapis.com/auth/documents",
                       "https://www.googleapis.com/auth/drive"],
                    "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
                    "invalid": False,
                    "_class": "OAuth2Credentials",
                    "_module": "oauth2client.client"
                }
            if not os.path.exists(session_folder):
                os.mkdir(session_folder)

            with open(f'{session_folder}/token_{user_info["user_id"]}.json', 'w') as file:
                file.write(json.dumps(token_json))
        else:
            response = redirect(url_for(GOOGLE_LOGIN))
    except Exception as e:
        logging.error('%s raised an error', str(e))
        print(e)
        response = redirect(url_for(GOOGLE_LOGIN))
    return response
