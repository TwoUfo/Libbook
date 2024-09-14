from flask import request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .models import User
from .api_models import user_login_model, user_register_mosel, user_model
from .extensions import db, jwt, api

ns = Namespace("")

@ns.route('/test')
class Test(Resource):
    def get(self):
        return {"test": "hello world"}
    

@ns.route('/register')
class Register(Resource):
    @ns.expect(user_register_mosel)
    @ns.marshal_with(user_model)
    def post(self):
        
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        return new_user, 201
    
    
@ns.route('/login')
class Login(Resource):
    @ns.expect(user_login_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {"msg": "Невірне ім'я користувача або пароль!"}, 401

        access_token = create_access_token(identity=username)
        response = jsonify({"msg": "Logged in"})
        response.set_cookie('access_token_cookie', access_token, httponly=True)
        return response
    
    

@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({"msg": "Logged out"})
        unset_jwt_cookies(response)
        return response
    
    
@ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        response = jsonify({"logged_in_as": current_user})
        return {"logged_in_as": current_user}, 200