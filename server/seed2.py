from config import app
from models import *
from faker import Faker
import random

fake=Faker()

AUTHORS = [
    'SpongeBob SquarePants',
    'Patrick Star',
    'Squidward Tentacles',
    'Sandy Cheeks',
    'Eugene Krabs',
    'Gary the Snail',
    'Sheldon Plankton'
]

COMMENTERS = [
    "Karen Plankton",
    "Mermaid Man",
    "Barnacle Boy",
    "Mrs. Puff",
    "Pearl Krabs",
    "Larry Lobster",
    "Bubble Bass",
    "King Neptune"
]

def clear_table():
    Post.query.delete()
    Comment.query.delete()
    db.session.commit()
    
def seed_posts():
    POST_SEED_SIZE = 28
    print(f"Generating posts: ", end="", flush=True)
    posts = []
    for n in range(POST_SEED_SIZE):
        new_post = Post(
            title=fake.sentence().title()[0:-1],
            content=" ".join(fake.paragraphs()),
            author=random.choice(AUTHORS)
        )
        posts.append(new_post)
        print(".", end="" if n < POST_SEED_SIZE - 1 else "\n", flush=True)
    db.session.add_all(posts)
    db.session.commit()
    
def seed_comments():
    MAX_COMMENT_SEED_SIZE = 15
    print(f"Generating comments: ", end="", flush=True)
    comments = []
    for post in Post.query.all():
        comment_seed_size = random.randint(1, MAX_COMMENT_SEED_SIZE)
        for n in range(comment_seed_size):
            new_comment = Comment(
                content=fake.paragraph(),
                commenter=random.choice(COMMENTERS),
                post_id=post.id
            )
            comments.append(new_comment)
            print(".", end="" if n < comment_seed_size - 1 else "\n", flush=True)
    db.session.add_all(comments)
    db.session.commit()
    
with app.app_context():
    clear_table()
    seed_posts()
    seed_comments()