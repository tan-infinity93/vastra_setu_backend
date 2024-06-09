"""
"""

# Import Modules:

import time
import json
from os import environ as env
from datetime import datetime
from urllib.parse import urlparse
from flask import current_app as c_app
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config.db_queries import QUERIES

# Class Definitions:

class FlaskPostgreSQL:
	"""
	"""
	def __init__(self, app=None, config_prefix="DB_CONNECTION", **kwargs):
		"""
		"""
		self.config_prefix = config_prefix

		if app is not None:
			self.init_app(app)

	def init_app(self, app, **kwargs):
		"""
		"""
		try:
			db_url = app.config.get("DB_URL")
			db_max_pool_size = app.config.get("DB_MAX_POOL_SIZE")
			db_params = urlparse(db_url)
			print(db_params)
			user = db_params.username
			password = db_params.password
			host = db_params.hostname
			port = db_params.port
			database = db_params.path[1:]

			connection_pool = psycopg2.pool.ThreadedConnectionPool(
				1, db_max_pool_size, 
				user=user,
				password=password,
				host=host,
				port=port,
				database=database
			)
			app.config["CONNECTION_POOL"] = connection_pool

			if env.get("DATABASE_TABLES_SETUP") == 'true':
				FlaskPostgreSQL.setup_tables(app)
				pass

		except Exception as e:
			raise e

	@staticmethod
	def get_table_names():
		"""
		"""
		try:
			table_names = list(QUERIES.keys())
			print(f'table_names: {table_names}')
			return table_names

		except Exception as e:
			raise e

	@staticmethod
	def setup_tables(app):
		"""
		"""
		try:
			table_names = FlaskPostgreSQL.get_table_names()
			with app.app_context():
				for table in table_names:
					drop_query = QUERIES.get(table).get('DROP')
					print(drop_query)
					FlaskPostgreSQL.execute_query(drop_query, app)
					# time.sleep(0.5)
					create_query = QUERIES.get(table).get('CREATE')
					print(create_query)
					FlaskPostgreSQL.execute_query(create_query, app)
					time.sleep(0.5)

		except Exception as e:
			raise e

	@staticmethod
	def get_sequence_id(sequence_name):
		"""
		"""
		try:
			connection_pool = c_app.config.get("CONNECTION_POOL")
			connection = connection_pool.getconn()
			if connection:
				cursor = connection.cursor()
				query = f"SELECT nextval('{sequence_name}')"
				# print(f'query: {query}')
				cursor.execute(f"{query}")
				results = cursor.fetchone()
				cursor.close()
				connection_pool.putconn(connection)
				if results:
					return results[0]
				return ''
			else:
				return ''

		except Exception as e:
			raise e

	@staticmethod
	def fetch_data(query):
		"""
		"""
		try:
			connection_pool = c_app.config.get("CONNECTION_POOL")
			connection = connection_pool.getconn()
			print('\n')
			# print(connection)
			# print(query)

			if connection:
				cursor = connection.cursor(cursor_factory=RealDictCursor)
				cursor.execute(f"{query}")
				results = cursor.fetchall()
				records = [
					{k:v for k, v in record.items()} for record in results
				]
				cursor.close()
				connection_pool.putconn(connection)
				return records
			else:
				raise(Exception('Postgres Pool Expired'))

		except Exception as e:
			raise e

	@staticmethod
	def fetch_data_tuples(query, key):
		"""
		"""
		try:
			connection_pool = c_app.config.get("CONNECTION_POOL")
			connection = connection_pool.getconn()
			print('\n')
			# print(connection)
			# print(query)

			if connection:
				cursor = connection.cursor(cursor_factory=RealDictCursor)
				cursor.execute(f"{query}")
				results = cursor.fetchall()
				records = [
					record.get(key) for record in results
				]
				cursor.close()
				connection_pool.putconn(connection)
				return records
			else:
				raise(Exception('Postgres Pool Expired'))

		except Exception as e:
			raise e

	@staticmethod
	def execute_query(query, app=None):
		"""
		"""
		try:
			connection_pool = c_app.config.get("CONNECTION_POOL")
			connection = connection_pool.getconn()

			if connection:
				cursor = connection.cursor()
				cursor.execute(query)
				connection.commit()
				cursor.close()
				connection_pool.putconn(connection)
			else:
				raise(Exception('Postgres Pool Expired'))

		except Exception as e:
			raise e
