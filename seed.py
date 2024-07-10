from app import app, db
from models import User, BookClub, Membership
from datetime import datetime

with app.app_context():
    # Drop existing tables
    db.drop_all()
    # Create tables
    db.create_all()

    # Clear session
    db.session.remove()

    # Create some users 
    user1 = User(username='Smith', email='smith@gmail.com')
    user2 = User(username='Johnson', email='johnson@gmail.com')

    # Add users to the session and commit to get their IDs
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create some book clubs with correct parameters
    bookclub1 = BookClub(name='Book Club 1', description='A book club for discussing fiction books.', cover_image='cover1.jpg', admin_id=user1.id)
    bookclub2 = BookClub(name='Book Club 2', description='A book club for discussing non-fiction books.', cover_image='cover2.jpg', admin_id=user2.id)

    # Add book clubs to the session and commit
    db.session.add(bookclub1)
    db.session.add(bookclub2)
    db.session.commit()