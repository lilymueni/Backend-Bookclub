from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import MetaData, Column, Integer, String, Text, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy

# Metadata with naming convention
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    }
)

# Initialize SQLAlchemy with the specified metadata
db = SQLAlchemy(metadata=metadata)

# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # Define columns
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80), nullable=False, unique=True)
    email = db.Column(String(120), nullable=False, unique=True)
    
    # Relationships
    book_clubs = db.relationship('BookClub', back_populates='admin')
    memberships = db.relationship('Membership', back_populates='user')
    
    # Association Proxy
    book_clubs_joined = association_proxy('memberships', 'book_club')
    
    # Serialization rules
    serialize_only = ("id", "username", "email")
    serialize_rules = ("-book_clubs", "-memberships")
    
    def __repr__(self):
        return f'User {self.username} is created successfully'

# BookClub Model
class BookClub(db.Model, SerializerMixin):
    __tablename__ = 'book_clubs'

    # Define columns
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    description = db.Column(Text, nullable=True)
    cover_image = db.Column(String(250), nullable=True)
    admin_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    admin = db.relationship('User', back_populates='book_clubs')
    memberships = db.relationship('Membership', back_populates='book_club')
    
    # Association Proxy
    members = association_proxy('memberships', 'user')

    # Serialization rules
    serialize_only = ("id", "name", "description", "cover_image", "admin_id")
    serialize_rules = ("-admin", "-memberships", "-members")

    def __repr__(self):
        return f'BookClub {self.name} is created successfully'

# Membership Model (join table)
class Membership(db.Model, SerializerMixin):
    __tablename__ = 'memberships'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    book_club_id = db.Column(db.Integer, ForeignKey('book_clubs.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False) 

    # Relationships
    user = db.relationship('User', back_populates='memberships')
    book_club = db.relationship('BookClub', back_populates='memberships')

    def __repr__(self):
        return f'Membership with User {self.user_id} in BookClub {self.book_club_id} as {self.role} is created successfully'
    
# Comment Model
class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'  # Table names should generally be in lowercase

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    
    # Relationships
    book_club_id = db.Column(db.Integer, db.ForeignKey('book_clubs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_club = db.relationship('BookClub', backref=db.backref('comments', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('comments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Comment {self.title} by User {self.user_id} in BookClub {self.book_club_id} created at {self.created_at}'
