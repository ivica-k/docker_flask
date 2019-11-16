import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import app


class TestDevelopmentConfig(TestCase):
	def create_app(self):
		app.config.from_object("project.config.Development")

		return app

	def test_app_is_development(self):
		self.assertTrue(app.config.get("SECRET_KEY") == "my_precious")
		self.assertFalse(current_app is None)
		self.assertTrue(
			app.config.get("DB_URL") == os.environ.get("DATABASE_URL")
		)