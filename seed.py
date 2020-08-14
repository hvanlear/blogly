""" Basic Test Data """

from models import User, Post, db, Tag, PostTag

from app import app


db.drop_all()
db.create_all()


mike = User(first_name='mike', last_name='sample')
jeff = User(first_name='jeff', last_name='sample1')
larry = User(first_name='larry', last_name='sample2')
bob = User(first_name='bob', last_name='sample3')
lucy = User(first_name='lucy', last_name='sample4')

post1 = Post(title='Post 1 Title',
             content='Post 1 Content Lorem Epsum some stuff', user_id=1)
post2 = Post(title='Post 2 Title',
             content='Post 2 Content Lorem Epsum some stuff', user_id=2)

tag1 = Tag(name='Funny')
tag2 = Tag(name='Sad')
tag3 = Tag(name='Wholesome')

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=2)
pt4 = PostTag(post_id=2, tag_id=3)


db.session.add_all([mike, jeff, larry, bob, lucy])
db.session.commit()

db.session.add_all([post1, post2])
db.session.commit()

db.session.add_all([tag1, tag2, tag3])
db.session.commit()

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()
