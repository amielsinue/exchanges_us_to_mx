from flask_restful import fields

user_auth = {
    "id": fields.Integer,
    "email": fields.String,
    "api_token": fields.String,
}