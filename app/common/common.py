import functools
import json

from flask import Response


def error_handler(f):
    """
    Handler to process exceptions for routes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except AttributeError:
            invalid_msg = {
                'error': 'No such user found'
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        except ValueError:
            invalid_msg = {
                'error': 'Incorrect value passed'
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        except Exception as e:
            invalid_msg = {
                'error': str(e)
            }
            response = Response(json.dumps(invalid_msg), status=400, mimetype='application/json')
        finally:
            return response

    return wrapper
