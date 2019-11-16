from flask import Blueprint
from flask_restful import Resource, Api


users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


class UserPing(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!"
        }


api.add_resource(UserPing, "/users/ping")