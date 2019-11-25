import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])


    def test_add_user(self):
        user = add_user("ivica", "ivica@server.com")
        with self.client:
            response = self.client.get(f'/users/{user.id}')

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn("success", data.get("status"))
            self.assertIn("ivica", data.get("data").get("username"))
            self.assertIn("ivica@server.com", data.get("data").get("email"))

            db.session.query(User).filter(User.id == user.id).delete()
            db.session.commit()


    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps({
                    "username": "ivica",
                    "email": "ivica@server.com",
                }),
                content_type="application/json"
            )
            response = self.client.post(
                "/users",
                data=json.dumps({
                    "username": "ivica",
                    "email": "ivica@server.com",
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("User already exists", data.get("message"))
            self.assertIn("fail", data.get("status"))


    def test_add_user_empty_json(self):
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid JSON", data.get("message"))
            self.assertIn("fail", data.get("status"))


    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({
                    "username": "ivica",
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid JSON", data.get("message"))
            self.assertIn("fail", data.get("status"))


    def test_get_single_user(self):
        user = User(username="ivica", email="ivica@server.com")
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("ivica", data.get("data").get("username"))
            self.assertIn("ivica@server.com", data.get("data").get("email"))
            self.assertIn("success", data.get("status"))


    def test_get_single_user_no_id(self):
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("fail", data.get("status"))
            self.assertIn("User does not exist", data.get("message"))


    def test_get_single_user_wrong_id(self):
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("fail", data.get("status"))
            self.assertIn("User does not exist", data.get("message"))


    def test_all_users(self):
        db.session.query(User).delete()
        db.session.commit()

        add_user("ivica", "ivica@server.com")
        add_user("marica", "marica@server.com")

        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())

            users = data.get("data").get("users")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(users), 2)
            self.assertIn(
                users[0].get("username"),
                "ivica"
            )
            self.assertIn(
                users[1].get("username"),
                "marica"
            )

            self.assertIn("success", data.get("status"))




if __name__ == "__main__":
    unittest.main()