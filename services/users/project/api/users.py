from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from project import db
from project.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


class UserPing(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!"
        }


class UserAdd(Resource):
    def post(self):
        post_data = request.get_json()

        response_object = {
            "status": "fail",
            "message": "Invalid JSON",
        }

        if not post_data:
            return response_object, 400

        username = post_data.get("username")
        email = post_data.get("email")

        try:
            user = User.query.filter_by(email=email).first()

            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()

                response_object["message"] = f"{email} added",
                response_object["status"] = "success"

                return response_object, 201

            else:
                response_object["message"] = "User already exists"

                return response_object, 400

        except exc.IntegrityError:
            db.session.rollback()

            return response_object, 400


class Users(Resource):
    def get(self, user_id):

        response_object = {
            "status":  "fail",
            "message": "User does not exist",
        }

        try:
            user = User.query.filter_by(id=user_id).first()

            if not user:
                return response_object, 404

            else:

                response_object = {
                    "status": "success",
                    "data": user.to_json()
                }

            return response_object, 200


        except exc.DataError:
            # db.session.rollback()

            return response_object, 404


class UsersList(Resource):
    def get(self):
        response_object = {
            "status": "success",
            "data": {
                "users": [user.to_json() for user in User.query.all()]
            }
        }

        return response_object, 200


api.add_resource(UserPing, "/users/ping")
api.add_resource(UserAdd, "/users")
api.add_resource(Users, "/users/<user_id>")
api.add_resource(UsersList, "/users")