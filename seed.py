from app import app, db
from models import User, BookClub, Membership, Comment
from datetime import datetime

# Function to seed the database
def seed_database():
    with app.app_context():
        # Drop existing tables
        db.drop_all()
        # Create tables
        db.create_all()

        # Clear session
        db.session.remove()

        # Create users
        user1 = User(username='alice', email='alice@example.com')
        user1.password_hash = "user1"
        user2 = User(username='bob', email='bob@example.com')
        user2.password_hash = "user2"
        user3 = User(username='jean', email='jean@example.com')
        user3.password_hash = "user3"
        

        # Create book clubs
        book_club1 = BookClub(name='Python Enthusiasts', description='A club for Python lovers', admin=user1)
        book_club2 = BookClub(name='Book Readers Club', description='Read and discuss books', admin=user2)

        # Create memberships
        membership1 = Membership(user=user1, book_club=book_club1, role='admin')
        membership2 = Membership(user=user2, book_club=book_club2, role='admin')
        membership3 = Membership(user=user3, book_club=book_club2, role='member')

        # Create comments
        comment1 = Comment(title='Great book!', content='I really enjoyed reading this.', user=user1, book_club=book_club1)
        comment2 = Comment(title='Interesting discussion', content='Looking forward to the next meeting.', user=user2, book_club=book_club2)

        # Add records to the session
        db.session.add_all([user1, user2, user3, book_club1, book_club2, membership1, membership2, membership3, comment1, comment2])
        db.session.commit()

        print("Database seeded successfully!")

# Run the seeding function
if __name__ == '__main__':
    seed_database()