import json
from api import app, db
from flask import Blueprint, request
from flask import jsonify
import api.auth_utils as auth_utils
import api.auth_tokens as auth_tokens
from api.auth_tokens import token_required
from api.utils import create_response, row_constructor
from api.models import User


mod = Blueprint('auth', __name__)

SIGNUP_URL = '/signup'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'


@app.route(SIGNUP_URL, methods=['POST'])
def create_account():
    request_json = request.get_json()

    keys = set(['username', 'password', 'accepts_email', 'email',
            'custom_email_subject', 'custom_email_body'])
    missing_keys = keys - set(request_json.keys())
    if missing_keys:
        return create_response(status=400,
                message='request json is missing the following keys: {}'\
                .format(missing_keys))

    username = request_json['username']
    password = request_json['password']
    accepts_email = request_json['accepts_email']
    email = request_json['email']
    custom_email_subject = request_json['custom_email_subject']
    custom_email_body = request_json['custom_email_body']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return create_response(status=400,
                message='username "{}" is already taken'.format(username))

    password_fail_message = auth_utils.validate_password_requirements(password)
    if password_fail_message:
        return create_response(status=400, message=password_fail_message)

    salt = auth_utils.generate_salt()
    hashed_password = auth_utils.hash_password(password, salt)
    new_user = User(username=username, accepts_email=accepts_email, email=email,
                    custom_email_subject=custom_email_subject,
                    custom_email_body=custom_email_body,
                    salt=salt, pw_hash=hashed_password)

    db.session.add(new_user)
    db.session.flush()
    new_user_id = new_user.id
    db.session.commit()

    token = auth_tokens.generate_token()
    while not auth_tokens.register_token(token, new_user_id):
        token = auth_tokens.generate_token()

    new_user.id = new_user_id
    response_data = new_user.to_dict()
    response_data.pop('pw_hash')
    response_data.pop('salt')
    response_data['token'] = token
    return create_response(data=response_data, status=201,
                            message='successfully created account')


@app.route(LOGIN_URL, methods=['POST'])
def log_in_user():
    request_json = request.get_json()

    try:
        username = request_json['username']
        password = request_json['password']
    except KeyError:
        return create_response(status=400,
                message='request json is missing username or password')

    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response(status=400, message='Incorrect login info')

    if auth_tokens.token_exists_for_user(user.id):
        return create_response(status=400,
                message='User "{}" is already logged in'.format(username))

    hashed_password = auth_utils.hash_password(password, user.salt)
    if hashed_password != user.pw_hash:
        return create_response(status=400, message='Incorrect login info')

    token = auth_tokens.generate_token()
    while not auth_tokens.register_token(token, user.id):
        token = auth_tokens.generate_token()

    return create_response(data={'token': token}, status=200,
                message='Log in success')


@app.route(LOGOUT_URL, methods=['POST'])
@token_required
def log_out_user():
    token = request.headers.get(auth_tokens.AUTH_TOKEN_HEADER_NAME)
    auth_tokens.delete_token(token)
    return create_response(status=200, message='successfully logged out')


@app.route('/tokens', methods=['GET'])
def check_tokens():
    return create_response(data=auth_tokens.active_tokens)


@app.route('/test-token-required', methods=['GET'])
@token_required
def example_route_with_automatic_token_check():
    return create_response(status=200, message='success with auto token check!')
