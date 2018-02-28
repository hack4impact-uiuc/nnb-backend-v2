import json
from flask import jsonify

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response

    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    if type(data) is not dict:
        raise TypeError('Data should be a dictionary 😞')

    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status

def row_constructor(RowClass, row_dict={}, **kwargs):
    """
    Creates a new row by making a new instance of RowClass out of row_dict and kwargs
    Ignores key-value pairs with list values
    """
    valid_row_dict = dict((key, val) for key, val in row_dict.items() if type(val) is not list)
    return RowClass(**valid_row_dict, **kwargs)

class Mixin():

    def to_dict(self):
        d_out = dict((key, val) for key, val in self.__dict__.items())
        d_out.pop('_sa_instance_state', None)
        d_out['_id'] = d_out.pop('id', None)  # rename id key to interface with response
        return d_out

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv