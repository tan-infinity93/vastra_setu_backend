"""
"""

# Import Modules:

import json
import redis
from datetime import datetime
from urllib.parse import urlparse
from itertools import zip_longest
from flask import current_app as c_app


# Class Definitions:

class FlaskRedis:
	"""
	"""
	def __init__(self, app=None, config_prefix="REDIS_CONNECTION", **kwargs):
			"""
			"""
			self.config_prefix = config_prefix

			if app is not None:
				self.init_app(app)

	def init_app(self, app, **kwargs):
		"""
		"""
		try:
			redis_url = app.config.get("REDIS_URL")
			redis_ssl = app.config.get("REDIS_SSL")
			redis_params = urlparse(redis_url)
			# print(redis_params)
			user = redis_params.username
			password = redis_params.password
			host = redis_params.hostname
			port = redis_params.port
			database = redis_params.path[1:]

			redis_config = {
			    'host': host,
			    'port': port,
			    'db': database,
			    'password': password if password else None,
			    'decode_responses': True
			}
			if redis_ssl == True:
			    redis_config['connection_class'] = redis.SSLConnection

			redis_pool = redis.ConnectionPool(**redis_config)
			redis_conn = redis.Redis(connection_pool=redis_pool)
			app.config['REDIS_CONN'] = redis_conn
			app.config['REDIS_POOL'] = redis_pool
		
		except Exception as e:
			raise e
