from flask_restx import fields
from .extensions import api

user_model = api.model('User', {
    "id": fields.Integer,
    'username': fields.String(required=True),
    'email': fields.String(required=True),
})

user_register_mosel = api.model('User', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),

})

user_login_model = api.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})
