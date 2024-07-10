from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin 
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime 

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)

# User Model
class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    #password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    # Relationships
    # One-to-Many: A user can create many book clubs
    book_clubs = db.relationship('BookClub', back_populates='admin')
    
    # One-to-Many: A user can have many memberships
    memberships = db.relationship('Membership', back_populates='user')
    
    # Association Proxy: Access book clubs a user has joined via memberships
    book_clubs_joined = association_proxy('memberships', 'book_club')

    def __repr__(self):
        return f'User {self.username} is created successfully'


# BookClub Model
class BookClub(db.Model,SerializerMixin):
    __tablename__ = 'book_clubs'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(250), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # Many-to-One: A book club is managed by one admin (User)
    admin = db.relationship('User', back_populates='book_clubs')
    
    # One-to-Many: A book club can have many memberships
    memberships = db.relationship('Membership', back_populates='book_club')
    
    # Association Proxy: Access members of a book club via memberships
    members = association_proxy('memberships', 'user')

    def __repr__(self):
        return f'BookClub {self.name} is created successfully'


# Membership Model (join table)
class Membership(db.Model,SerializerMixin):
    __tablename__ = 'memberships'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_club_id = db.Column(db.Integer, db.ForeignKey('book_clubs.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False) 
    # Relationships
    # Many-to-One: A membership belongs to one user
    user = db.relationship('User', back_populates='memberships')
    
    # Many-to-One: A membership belongs to one book club
    book_club = db.relationship('BookClub', back_populates='memberships')

    def __repr__(self):
        return f'Membership with User {self.user_id} in BookClub {self.book_club_id} as {self.role} is created successfully'


# Discussion Model
class Discussion(db.Model, SerializerMixin):
    __tablename__ = 'discussions'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    # Relationships
    book_club_id = db.Column(db.Integer, db.ForeignKey('book_clubs.id'), nullable=False)
    book_club = db.relationship('BookClub', backref=db.backref('discussions', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Discussion {self.title} in BookClub {self.book_club_id} created at {self.created_at}'
