'''
'''

# Import Modules:

import os
from pprint import PrettyPrinter
from flask import Flask, request, make_response, render_template
from flask_cors import CORS
from flask_restful import Api
from config import get_config

# Create Flask App Factory:

def create_app(config_name):
	app = Flask(
		__name__, 
		template_folder='../templates/', 
		static_folder='../static/'
	)
	CORS(app)
	app.config.update(get_config(config_name))

	# App Binding:

	"""
		Use / Enable below modules as needed
	"""

	"""
	from bindings.flask_postgresql import FlaskPostgreSQL
	from bindings.flask_redis import FlaskRedis

	flaskpostgresql_app = FlaskPostgreSQL()
	flaskpostgresql_app.init_app(app)

	flaskredis_app = FlaskRedis()
	flaskredis_app.init_app(app)
	"""

	api = Api(app, catch_all_404s=True)
	pp = PrettyPrinter(indent=4)
	app.config['pprint'] = pp
	pp.pprint(app.config)

	# Add API Routes:

	from routes.healthcheck import Healthcheck

	api.add_resource(
		Healthcheck, '/', 
		methods=['GET'], 
		endpoint='healthcheck_api_root'
	)
	api.add_resource(
		Healthcheck, '/v1/healthcheck', 
		methods=['GET'], 
		endpoint='healthcheck_api'
	)

	return app
