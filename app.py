#!/usr/bin/env python3
import os

from flask import Flask, request, make_response, jsonify, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, BookClub, Membership, Discussion

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  
# app.secret_key = os.urandom(24)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

#before any request, to determine the page to render

@app.before_request
def check_if_logged_in():
    open_access_list = [
        'signup',
        'login',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):
        return {'error': '401 Unauthorized'}, 401

class CheckSession(Resource):

    def get(self):
        
        user_id = session['user_id']
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        return {}, 401
class Login(Resource):
    def post(self):
        username = request.form.get('username')
        email= request.form.get('email')
    
        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(email):
            session['user_id'] = user.id
            welcome_message = f"Welcome {user.username}"
            return jsonify({
                'message': welcome_message,
                'id': user.id,
                'username': user.username,
                "email":user.email
            }), 200
        return {"error": "Invalid username or email"}, 401

# User Signup
class Signup(Resource):
    def post(self):
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')
        
        
        if not all([username, password]):
            return {'error': '422 Unprocessable Entity'}, 422

        user = User(
            username=username
        )

        # the setter will encrypt this
        user.password_hash = password

        try:

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(), 201

        except IntegrityError:

            return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):

    def get(self):
        
        user_id = session['user_id']
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        return {}, 401

# # User Login
# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         user = User.query.filter_by(username=data['username']).first()
#         if user and check_password_hash(user.password_hash, data['password']):
#             session['user_id'] = user.id
#             return jsonify(user.to_dict()), 200
#         return {"error": "invalid username or password"}, 401

# User Logout
class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return {"message": "Logged out successfully"}, 200
class Test(Resource):
    def get(self):
        return make_response("message""Working")
# CRUD for Users
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        response = make_response(jsonify(users), 200)
        return response

## CRUD for BookClubs
class BookClubs(Resource):
    def get(self):
        books = [book.to_dict() for book in BookClub.query.all()]
        response = make_response(jsonify(books), 200)  # Corrected this line
        return response

    def post(self):
        data = request.get_json()
        new_book_club = BookClub(
            name=data['name'],
            description=data.get('description'),
            cover_image=data.get('cover_image'),
            admin_id=session.get('user_id')
        )
        db.session.add(new_book_club)
        db.session.commit()
        return jsonify(new_book_club.to_dict()), 201

# CRUD for Discussions
class Discussions(Resource):
    def get(self):
        discussions = Discussion.query.all()
        return jsonify([discussion.to_dict() for discussion in discussions])

    def post(self):
        data = request.get_json()
        new_discussion = Discussion(
            content=data['content'],
            user_id=session.get('user_id'),
            book_club_id=data['book_club_id']
        )
        db.session.add(new_discussion)
        db.session.commit()
        return jsonify(new_discussion.to_dict()), 201

# Resource routing
api.add_resource(Test, '/test', endpoint='test')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Users, '/users', endpoint='users')
api.add_resource(BookClubs, '/book_clubs', endpoint='book_clubs')
api.add_resource(Discussions, '/discussions', endpoint='discussions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
