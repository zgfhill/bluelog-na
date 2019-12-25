import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog import db
from bluelog.models import Admin, Category, Post, Comment, Link

fake = Faker('zh_CN')

def fake_admin():
	admin = Admin(username='admin', blog_title='Bluelogg', blog_sub_title='No, i am the real thing.', name='Garifeld Chow', about='Um, should there must be somthing?')
	admin.set_password('password')
	db.session.add(admin)
	db.session.commit()

def fake_categories(count=10):
	category = Category(name='Default')
	db.session.add(category)

	for i in range(count):
		category = Category(name=fake.word())
		db.session.add(category)
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

def fake_posts(count=50):
	for i in range(count):
		post = Post(title=fake.sentence(), body=fake.text(2000), timestamp=fake.date_time(), category=Category.query.get(random.randint(1, Category.query.count())))
		db.session.add(post)
	db.session.commit()

def fake_comments(count=500):
	for i in range(count):
		comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(), reviewed=True, timestamp=fake.date_time(), post=Post.query.get(random.randint(1, Post.query.count())))
		db.session.add(comment)
	db.session.commit()

	for i in range(int(count * .1)):
		comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(), reviewed=False, timestamp=fake.date_time(), post=Post.query.get(random.randint(1, Post.query.count())))
		db.session.add(comment)
	
		comment = Comment(author='Garifeld Chow', email='garfieldchow@hotmail.com', site='www.laonana.com', body=fake.sentence(), from_admin=True, reviewed=True, timestamp=fake.date_time(), post=Post.query.get(random.randint(1, Post.query.count())))
		db.session.add(comment)
	db.session.commit()

	for i in range(count):
		comment = Comment(author=fake.name(), email=fake.email(), site=fake.url(), body=fake.sentence(), reviewed=True, timestamp=fake.date_time(), post=Post.query.get(random.randint(1, Post.query.count())), replied=Comment.query.get(random.randint(1, Comment.query.count())))
		db.session.add(comment)
	db.session.commit()

def fake_links():
	qq = Link(name='Qq', url='http://www.qq.com')
	baidu = Link(name='Baidu', url='http://www.baidu.com')
	sohu = Link(name='Sohu', url='http://www.sohu.com')
	sina = Link(name='Sina', url='http://www.sina.cn')
	db.session.add_all([qq, baidu, sohu, sina])
	db.session.commit()
