from functools import wraps

from flask import jsonify


def handle_all_exceptions(f):
    @wraps(f)
    def applicator(*args, **kwargs):
      try:
         return f(*args, **kwargs)
      except Exception as err:
        _error = {
          "status": False,
          "error": f"Error : please check logs"
        }
        return jsonify(_error)
    return applicator
