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

SIGNUP_URL = '/auth/signup'
LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
TEST_URL = '/auth/test-token-required'

@app.route(SIGNUP_URL, methods=['POST'])
def create_account():
    request_json = request.get_json()

    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if request_json.get(field) is None]
    if len(missing_fields):
        return create_response(
            status=400,
            message='Request json is missing the following fields: {}' \
            .format(', '.join(missing_fields))
        )

    username = request_json.get('username')
    password = request_json.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        return create_response(
            status=400,
            message='Username "{}" is already taken'.format(username)
        )

    password_fail_message = auth_utils.validate_password_requirements(password)
    if password_fail_message:
        return create_response(status=400, message=password_fail_message)

    salt = auth_utils.generate_salt()
    hashed_password = auth_utils.hash_password(password, salt)
    user_add = {
        'username': username,
        'salt': salt,
        'pw_hash': hashed_password
    }
    new_user = row_constructor(User, user_add)

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
    return create_response(
        data=response_data,
        status=201, 
        message='Successfully created account'
    )

@app.route(LOGIN_URL, methods=['POST'])
def log_in_user():
    request_json = request.get_json()
    INCORRECT_INFO_MSG = 'Incorrect login info'

    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if request_json.get(field) is None]
    if len(missing_fields):
        return create_response(
            status=400,
            message='Request json is missing the following fields: {}' \
            .format(', '.join(missing_fields))
        )

    username = request_json.get('username')
    password = request_json.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return create_response(status=400, message=INCORRECT_INFO_MSG)

    token = auth_tokens.token_exists_for_user(user.id)
    if token:
        return create_response(
            data={'token': token},
            status=200,
            message='Log in success'
        )

    hashed_password = auth_utils.hash_password(password, user.salt)
    if hashed_password != user.pw_hash:
        return create_response(status=400, message=INCORRECT_INFO_MSG)

    token = auth_tokens.generate_token()
    while not auth_tokens.register_token(token, user.id):
        token = auth_tokens.generate_token()

    return create_response(
        data={'token': token},
        status=200,
        message='Log in success'
    )

@app.route(LOGOUT_URL, methods=['POST'])
@token_required
def log_out_user():
    token = request.headers.get(auth_tokens.AUTH_TOKEN_HEADER_NAME)
    # success = auth_tokens.delete_token(token)
    success = True
    if success:
        return create_response(status=200, message='Successfully logged out')
    return create_response(status=400, message='Invalid token')

@app.route(TEST_URL, methods=['GET'])
@token_required
def example_route_with_automatic_token_check():
    return create_response(status=200, message='Success with auto token check!')
