from app import app, db
from models import User, BookClub, Membership, Comment
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
    bookclub1 = BookClub(
        name='Book Club 1', 
        description='A book club for discussing fiction books.', 
        cover_image='cover1.jpg', 
        admin_id=user1.id
    )
    bookclub2 = BookClub(
        name='Book Club 2', 
        description='A book club for discussing non-fiction books.', 
        cover_image='cover2.jpg', 
        admin_id=user2.id
    )

    # Add book clubs to the session and commit
    db.session.add(bookclub1)
    db.session.add(bookclub2)
    db.session.commit()

    # Create some comments related to book clubs and users
    comment1 = Comment(
        title='First Comment',
        content='I enjoyed reading tis book!.',
        created_at=datetime.utcnow(),
        book_club_id=bookclub1.id,
        user_id=user1.id
    )
    comment2 = Comment(
        title='First Comment',
        content='The author did i great job,quite an interesting read!',
        created_at=datetime.utcnow(),
        book_club_id=bookclub2.id,
        user_id=user2.id
    )
    comment3 = Comment(
        title='Second Comment',
        content='Took me time to finish this book, I kinda struggled reading it!',
        created_at=datetime.utcnow(),
        book_club_id=bookclub1.id,
        user_id=user2.id
    )

    # Add comments to the session and commit
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)
    db.session.commit()
