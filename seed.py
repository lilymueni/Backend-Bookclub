from app import app
from models import db, User, BookClub, Membership, Comment
from faker import Faker
from random import choice, randint

fake = Faker()

# Function to create users
def create_users(num):
    users = []
    for _ in range(num):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.password_hash = fake.password() 
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

# Function to create book clubs
def create_book_clubs(num):
    book_clubs = []
    for _ in range(num):
        book_club = BookClub(
            name=fake.company(),
            description=fake.text(),
            cover_image=fake.image_url(),
            genre=fake.word()
        )
        book_clubs.append(book_club)
        db.session.add(book_club)
    db.session.commit()
    return book_clubs

# Function to create memberships
def create_memberships(users, book_clubs):
    roles = ['member', 'admin']
    memberships = []
    for _ in range(len(users) * 2):  # Each user can be a member of 2 book clubs
        membership = Membership(
            user_id=choice(users).id,
            book_club_id=choice(book_clubs).id,
            role=choice(roles)
        )
        memberships.append(membership)
        db.session.add(membership)
    db.session.commit()
    return memberships

# Function to create comments
def create_comments(users, book_clubs, num):
    comments = []
    for _ in range(num):
        comment = Comment(
            title=fake.sentence(),
            content=fake.text(),
            user_id=choice(users).id,
            book_club_id=choice(book_clubs).id,
            created_at=fake.date_time_this_year()
        )
        comments.append(comment)
        db.session.add(comment)
    db.session.commit()
    return comments

if __name__ == '__main__':
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Seeding users...")
        users = create_users(10)
        
        print("Seeding book clubs...")
        book_clubs = create_book_clubs(5)

        print("Seeding memberships...")
        create_memberships(users, book_clubs)

        print("Seeding comments...")
        create_comments(users, book_clubs, 20)

        print("Seeding completed.")
