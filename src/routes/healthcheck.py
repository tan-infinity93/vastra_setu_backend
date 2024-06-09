"""
"""

# Import Modules:

import traceback
from datetime import datetime
from flask import Flask, request, current_app as c_app, make_response
from routes.base_resource import BaseResource
from middleware.decorators import (
	rate_limit, check_args, check_json, check_auth
)

# Class Definitions:

class Healthcheck(BaseResource):
	"""
	"""
	# @rate_limit
	def get(self):
		"""
		"""
		try:
			response = {
				"meta": self.META,
				"message": f"welcome to {self.APP_NAME} api"
			}
			return response, self.SUCCESS_CODE, self.HEADERS

		except Exception as e:
			traceback.print_exc()
			response = {
				"meta": self.META,
				"message": "unable to process request",
				"reason": "internal server error"
			}
			return response, self.EXCEPTION_CODE, self.HEADERS
