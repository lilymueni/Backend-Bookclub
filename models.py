from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import validates  # Add this import for validates decorator
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)

    # Relationships
    book_clubs = db.relationship('BookClub', back_populates='admin')
    memberships = db.relationship('Membership', back_populates='user')

    # Association Proxy
    book_clubs_joined = association_proxy('memberships', 'book_club')

    # Serialization rules
    serialize_only = ("id", "username", "email")
    serialize_rules = ("-book_clubs", "-memberships")

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be empty")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty")
        return email

# BookClub Model
class BookClub(db.Model, SerializerMixin):
    __tablename__ = 'book_clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String(250), nullable=True)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    admin = db.relationship('User', back_populates='book_clubs')
    memberships = db.relationship('Membership', back_populates='book_club')
    
    # Association Proxy
    members = association_proxy('memberships', 'user')

    # Serialization rules
    serialize_only = ("id", "name", "description", "cover_image", "admin_id")
    serialize_rules = ("-admin", "-memberships", "-members")

    def __repr__(self):
        return f'BookClub {self.name}'

# Membership Model (join table)
class Membership(db.Model, SerializerMixin):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_club_id = Column(Integer, ForeignKey('book_clubs.id'), nullable=False)
    role = Column(String(50), nullable=False) 

    # Relationships
    user = db.relationship('User', back_populates='memberships')
    book_club = db.relationship('BookClub', back_populates='memberships')

    def __repr__(self):
        return f'Membership with User {self.user_id} in BookClub {self.book_club_id} as {self.role}'

# Comment Model
class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)  
    
    # Relationships
    book_club_id = Column(Integer, ForeignKey('book_clubs.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_club = db.relationship('BookClub', backref=db.backref('comments', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('comments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Comment {self.title} by User {self.user_id} in BookClub {self.book_club_id}'