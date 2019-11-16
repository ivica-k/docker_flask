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
            app.config.get("SQLALCHEMY_DATABASE_URI") == os.environ.get("DATABASE_URL")
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("project.config.Testing")
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config.get("SECRET_KEY") == "my_precious")
        self.assertTrue(app.config.get("TESTING"))
        self.assertFalse(app.config.get("PRESERVE_CONTEXT_ON_EXCEPTION"))
        self.assertTrue(
            app.config.get("SQLALCHEMY_DATABASE_URI") ==
            os.environ.get("DATABASE_TEST_URL")
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("project.config.Production")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config.get("SECRET_KEY") == "my_precious")
        self.assertFalse(app.config.get("TESTING"))


if __name__ == "__main__":
    unittest.main()