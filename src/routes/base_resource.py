"""
"""

# Import Modules:

import traceback
from datetime import datetime
from flask import Flask, request, current_app as c_app
from flask_restful import Resource

# Class Definitions:

class BaseResource(Resource):
    """
    """
    def __init__(self):
        """
        """
        self.META = {
            "version": 1.0,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.APP_NAME = c_app.config.get("PROJECT_NAME", "flask-app-template")
        self.HEADERS = {"Content-Type": "application/json"}
        self.SUCCESS_CODE = 200
        self.CREATED_CODE = 201
        self.BAD_CODE = 400
        self.AUTH_CODE = 401
        self.NOT_FOUND = 404
        self.PROCESS_ERROR_CODE = 422
        self.EXCEPTION_CODE = 500

    def get(self):
        """
        """
        pass

    def post(self):
        """
        """
        pass

    def put(self):
        """
        """
        pass

    def delete(self):
        """
        """
        pass