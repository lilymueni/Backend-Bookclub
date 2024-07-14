#!/usr/bin/env python3

# modified external database url  = postgresql://backend_2k0b_user:oQ9vyn6SwVXw9RVlfqgEChEcdCurwbIP@dpg-cq9purdds78s739h7lvg-a.oregon-postgres.render.com/bookclub_app_db

# export DATABASE_URI=postgresql://backend_2k0b_user:oQ9vyn6SwVXw9RVlfqgEChEcdCurwbIP@dpg-cq9purdds78s739h7lvg-a.oregon-postgres.render.com/bookclub_app_db

import os
#from dotenv import load_dotenv
from flask import Flask, request, make_response, jsonify, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, BookClub, Membership, Comment

#load_dotenv()  # Load environment variables from .env file
name = "Backend-Bookclub"
app = Flask(name)
CORS(app)

os.environ["DB_EXTERNAL_URL"] = "postgresql://backend_2k0b_user:oQ9vyn6SwVXw9RVlfqgEChEcdCurwbIP@dpg-cq9purdds78s739h7lvg-a.oregon-postgres.render.com/bookclub_app_db"
# Configure SQLAlchemy database URI based on environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up database URI based on environment (use DB_EXTERNAL_URL by default)
if os.getenv('FLASK_ENV') == 'production':
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_INTERNAL_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_EXTERNAL_URL")
    

# Print the SQLALCHEMY_DATABASE_URI to verify it's set correctly
print("SQLALCHEMY_DATABASE_URI:", app.config["SQLALCHEMY_DATABASE_URI"])

# Set the Flask app secret key from environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Before any request, to determine the page to render
""" @app.before_request
def check_if_logged_in():
    open_access_list = ['signup', 'login', 'check_session']
    if request.endpoint not in open_access_list and not session.get('user_id'):
        return {'error': '401 Unauthorized'}, 401 """

# Define resources and routes
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        return {}, 401

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            session['user_id'] = user.id
            return jsonify(user.to_dict()), 200
        return {"error": "invalid username or password"}, 401

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        if not all([username, email]):
            return {'error': '422 Unprocessable Entity'}, 422
        user = User(username=username, email=email)
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return user.to_dict(), 201
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422

class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return {"message": "Logged out successfully"}, 200

class Test(Resource):
    def get(self):
        return make_response("message", "Working")

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        response = make_response(jsonify(users), 200)
        return response

class BookClubs(Resource):
    def get(self):
        books = [book.to_dict() for book in BookClub.query.all()]
        response = make_response(jsonify(books), 200)
        return response

    def post(self):
        data = request.get_json()
        new_book_club = BookClub(
            name=data['name'],
            description=data.get('description'),
            cover_image=data.get('cover_image'),
            )
        db.session.add(new_book_club)
        db.session.commit()
        return jsonify(new_book_club.to_dict()), 201


#get a book club by id
class BookClubById(Resource):
    def get(self, id):
        bookClub = BookClub.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(bookClub), 200)
    #update a bookclub
    def patch(self, id):
        data = request.get_json()

        bookclub = BookClub.query.filter_by(id=id).first()

        for attr in data:
            setattr(bookclub, attr, data[attr])

        db.session.add(bookclub)
        db.session.commit()

        return make_response(bookclub.to_dict(), 200)

    def delete(self, id):
        bookclub = BookClub.query.filter_by(id=id).first()
        db.session.delete(bookclub)
        db.session.commit()

        return make_response('', 204)

class Comments(Resource):
    def get(self):
        comments = Comment.query.all()
        return jsonify([comment.to_dict() for comment in comments])


    def post(self):
            data = request.get_json()
            new_comment = Comment(
                content=data['content'],
                user_id=session.get('user_id'),
                book_club_id=data['book_club_id']
            )
            db.session.add(new_comment)
            db.session.commit()
            return jsonify(new_comment.to_dict()), 201

# Resource routing
api.add_resource(Test, '/test', endpoint='test')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Users, '/users', endpoint='users')
api.add_resource(BookClubs, '/book_clubs', endpoint='book_clubs')
api.add_resource(BookClubById, '/book_clubs/<int:id>')
api.add_resource(Comments, '/book_clubs/<int:id>/comments')


if name == 'main':
    app.run(port=5555, debug=True)
