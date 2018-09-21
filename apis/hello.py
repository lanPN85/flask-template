"""
Example API endpoint
"""

from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return 'Hello World'
