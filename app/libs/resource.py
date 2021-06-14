import json
from flask_restful import Resource, abort
from flask import request

_falsy = ['null', 'None', 'NULL', 'NONE', 'none', None, '', b'']


class BaseResource(Resource):

    @staticmethod
    def abort(code, **kwargs):
        abort(code, **kwargs)

    def __init__(self, *args, **kwargs):
        self.request = request
        try:
            if request.data not in _falsy:
                self.data = json.loads(request.data)
        except ValueError:
            abort(400, "Invalid JSON")
