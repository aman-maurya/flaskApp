""" Users  """
from flask import Blueprint
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.logger import LoggerUtils

user_v1 = Blueprint('user_v1', __name__)


class User(Resource):
    """ User Class """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    # def post(self):
    #     data = User.parser.parse_args()
    #
    #     if UserModel.find_by_username(data['username']):
    #         return {"message": "A user with that username already exists"}, 400
    #
    #     user = UserModel(**data)
    #     user.save_to_db()
    #
    #     return {"message": "User created successfully."}, 201
    #
    # def get(self):
    #     """ Get user Detail """
    #     return {"message": "hello world"}

    @user_v1.route('/list')
    def user_list() -> object:  # pylint: disable=E0211
        """
        Get user List
        :rtype: object
        """
        try:
            users_list = UserModel.find_all()
            return {"status": 1, "message": "", "data": users_list}
        except Exception as exc:
            LoggerUtils.error(exc)
