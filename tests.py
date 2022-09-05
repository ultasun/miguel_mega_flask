from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # transient database only

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='jim')
        u.set_password('homeless')
        self.assertFalse(u.check_password('homeowner'))
        self.assertTrue(u.check_password('homeless'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='jim', email='jim@example.com')
        u2 = User(username='cindy', email='cindy@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'cindy')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'jim')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='jim', email='jim@example.com')
        u2 = User(username='cindy', email='cindy@example.com')
        u3 = User(username='selina', email='selina@example.com')
        u4 = User(username='yeeny', email='yeeny@example.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body="post from jim", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from cindy", author=u2,
                  timestamp=now + timedelta(seconds=3))
        p3 = Post(body="post from selina", author=u3,
                  timestamp=now + timedelta(seconds=6))
        p4 = Post(body="post from yeeny", author=u4,
                  timestamp=now + timedelta(seconds=9))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u2.follow(u4)
        u3.follow(u4)
        u4.follow(u1)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        self.assertEqual(f1, [p3, p2, p1])
        self.assertEqual(f2, [p4, p2])
        self.assertEqual(f3, [p4, p3])
        self.assertEqual(f4, [p4, p1])

if __name__ == '__main__':
    unittest.main(verbosity=2)

