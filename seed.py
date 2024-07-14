from app import app, db
from models import User, BookClub, Membership, Comment
from datetime import datetime

# Function to seed the database
def seed_database():
    with app.app_context():

        
        Comment.query.delete()
        Membership.query.delete()
        User.query.delete()
        BookClub.query.delete()
        
        
        print("Deleted all records...")
        

        # Clear session
        """ db.session.remove() """


        # Create users
        
        user1 = User(username='alice', email='alice@example.com')
        user1.password_hash = "user1"
        user2 = User(username='bob', email='bob@example.com')
        user2.password_hash = "user2"
        user3 = User(username='jean', email='jean@example.com')
        user3.password_hash = "user3"
        user4 = User(username='Kelly', email='kelly@example.com')
        user4.password_hash = "1234"
        print("Created users")

        
        

        # Create book clubs
        book_club1 = BookClub(name='Python Enthusiasts', description='A club for Python lovers', cover_image="http.logo1.com", comments=[], memberships=[], genre = "Tourism" )
        book_club2 = BookClub(name='Book Readers Club', description='Read and discuss books', cover_image="http.logo1.com", comments=[], memberships=[],  genre = "Tourism")
        book_club3 = BookClub(name = "Cultural Identity", cover_image = "https://i.pinimg.com/736x/84/fa/16/84fa16af03cabbe487e9b87f3e724963.jpg", description = "Books exploring cultural heritage and identity.", genre = "Cultural Identity", memberships = [], comments = [])
        book_club4 = BookClub(name= "Fantasy and Mythology", cover_image = "https=//i.pinimg.com/736x/26/c9/52/26c9526963119cb7437e6dd8cbdd7f6f.jpg", description= "Books featuring fantastical worlds and mythological themes.", genre= "Fantasy and Mythology", memberships= [], comments= [])
        book_club5 = BookClub(name= "Adventure and Travel",cover_image="https=//i.pinimg.com/736x/e0/84/d6/e084d6df52e1c4ffa7dd2a8528393a21.jpg", description= "Travel guides and adventure stories.", genre= "Adventure and Travel",memberships= [], comments= [])
        book_club7 = BookClub(name= "Social Justice", cover_image="https=//i.pinimg.com/736x/28/8d/e3/288de3c1d0b35cc50bc018acb879573c.jpg", description= "Books focusing on social issues and activism.", genre= "Social Justice", memberships= [], comments= [])
        book_club6 = BookClub(name= "Romance", cover_image="https=//i.pinimg.com/736x/00/21/b5/0021b5139b25e0d9633c60cbf6d5e23c.jpg", description= "Love stories and romantic novels.", genre= "Romance", memberships= [], comments= [])
        
        print("Created bookclubs")

        

        # Create memberships
        membership1 = Membership(user=user1, book_club=book_club1, role='admin')
        membership2 = Membership(user=user2, book_club=book_club2, role='admin')
        membership3 = Membership(user=user3, book_club=book_club2, role='member')
        print("created memberships")

        # Create comments
        comment1 = Comment(title='Great book!', content='I really enjoyed reading this.', user=user1, book_club=book_club1)
        comment2 = Comment(title='Interesting discussion', content='Looking forward to the next meeting.', user=user2, book_club=book_club2)
        print("created comments")
        book_club1.comments.append(comment1)
        user1.comments.append(comment1)
        book_club2.comments.append(comment2)
        user2.comments.append(comment2)
        print("appended comments to the respective bookclubs and user")
        
        

        # Add records to the session, ive left out , """ membership1, membership2, membership3, comment1, comment2 """
        db.session.add_all([user1, user2, user3, user4, book_club1, book_club2, book_club3, book_club4, book_club5, book_club6, book_club7, membership1, membership2, membership3,comment1, comment2])
        db.session.commit()

        print("Database seeded successfully!")

# Run the seeding function
if __name__ == '__main__':
    seed_database()