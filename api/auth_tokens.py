import secrets
import datetime
from functools import wraps
from flask import request
from api.utils import create_response

AUTH_TOKEN_HEADER_NAME = 'auth-token'
AUTH_TOKEN_NUM_BYTES = 32
DEFAULT_EXPIRATION = datetime.timedelta(hours=1)

"""
auth_tokens = {
    <token string>: {
        'user_id': <user_id>,
        'expiration': <expiration timestamp of this token>
    }
}
"""
active_tokens = {}

def token_required(f):
    """This decorator checks to ensure that the token sent with a request
    exists and is not expired. Returns a failure response if the token does not
    exist. Deletes the token and returns a failure response if the token exists
    but is expired. Otherwise, sets the token expiration to DEFAULT_EXPIRATION
    time units from the current time.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get(AUTH_TOKEN_HEADER_NAME)

        if not token_exists(token):
            return create_response(
                data={'token': token},
                status=401,
                message='invalid authorization token'
            )
        if not is_valid_token(token):
            delete_token(token)
            return create_response(
                data={'token': token},
                status=401,
                message='expired authorization token'
            )

        update_token_expiration(token)

        return f(*args, **kwargs)

    return decorated

def generate_token():
    return secrets.token_hex(AUTH_TOKEN_NUM_BYTES)

def register_token(token, user_id):
    """Attempt to register a token for the given user. Returns True on success
    and False on failure."""
    if token in active_tokens:
        return False
    expiration = datetime.datetime.now() + DEFAULT_EXPIRATION
    active_tokens[token] = {
        'user_id': user_id,
        'expiration': expiration
    }
    return True

def token_exists(token):
    """Returns True if the given token exists in the tokens store. Returns
    False otherwise."""
    return token in active_tokens

def is_valid_token(token):
    """Returns True if the given token is valid and not expired.
    Returns False otherwise."""
    if token in active_tokens:
        return active_tokens[token]['expiration'] > datetime.datetime.now()
    return False

def update_token_expiration(token):
    """Attempt to update expiration timestamp of the given token.
    If the token is valid, adds DEFAULT_EXPIRATION many time units to the
    token's expiration timestamp and returns True. Otherwise returns False."""
    if token in active_tokens:
        expiration = datetime.datetime.now() + DEFAULT_EXPIRATION
        active_tokens[token]['expiration'] = expiration
        return True
    return False

def delete_token(token):
    """Attempt to invalidate the given token. Returns True if the token existed
    as an active token. Otherwise returns False."""
    if token in active_tokens:
        active_tokens.pop(token)
        return True
    return False

def token_exists_for_user(user_id):
    """Returns True if a valid, unexpired token exists for the given user.
    Returns False otherwise."""
    for token in active_tokens:
        if active_tokens[token]['user_id'] == user_id:
            return active_tokens[token]['expiration'] > datetime.datetime.now()
    return False

def get_user(token):
    """Returns the user_id associated with the given token. Returns None if the
    token is invalid or expired."""
    if token in active_tokens:
        if active_tokens[token]['expiration'] > datetime.datetime.now():
            return active_tokens[token]['user_id']
    return None
