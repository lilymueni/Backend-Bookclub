#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from datetime import timedelta
from werkzeug.exceptions import NotFound
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)

# Import your models after initializing db to avoid circular imports
from models import User, BookClub, Membership, Comment

@app.route('/example')
def example_route():
    try:
        result = 1 / 0  # Example division by zero error
        return jsonify(result=result), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({'error': 'NotFound', 'message': 'The requested resource does not exist'}),
        404
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.before_request
def check_login():
    allowed_endpoints = ['login', 'logout', 'sign_up', 'check_session']

    if request.endpoint in allowed_endpoints:
        return

    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found. Please log in again."}), 401

    request.user = user

    if request.endpoint == 'book_clubs' and user.role != 'admin':
        return jsonify({"error": "Unauthorized access. Admin role required."}), 403

class Login(Resource):
    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(email):
            session['user_id'] = user.id
            access_token = create_access_token(identity=user.id)
            return {
                'message': f"Welcome {user.username}",
                'access_token': access_token,
                'username': user.username,
                "email" : user.email
            }, 200
        else:
            return {"error": "Invalid username or email"}, 401

class Register(Resource):
    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')

        if not all([username, email]):
            return {'message': 'Username and email are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        new_user = User(username=username, email=email)

        db.session.add(new_user)
        db.session.commit()

        success_message = {'message': 'User registered successfully'}
        response = make_response(success_message)
        response.status_code = 201
        response.headers['Location'] = url_for('login')

        return response

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"error": "No active session"}), 401

        user = User.query.get(user_id)

        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"error": "User not found"}), 404

class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return jsonify({"message": "Logout successful"})

class BookClubs(Resource):
    def get(self):
        book_clubs = [club.to_dict() for club in BookClub.query.all()]
        return jsonify(book_clubs), 200

    def post(self):
        data = request.get_json()
        new_club = BookClub(
            name=data['name'],
            description=data.get('description'),
            cover_image=data.get('cover_image'),
            admin_id=session.get('user_id')
        )
        db.session.add(new_club)
        db.session.commit()
        return jsonify(new_club.to_dict()), 201

api.add_resource(Login, '/login')
api.add_resource(Register, '/sign_up')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(BookClubs, '/book_clubs')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
