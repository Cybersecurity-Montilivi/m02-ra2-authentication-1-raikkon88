import sys, os
from unittest import TestCase, mock, main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


environ = os.environ
environ["VOLUME_PATH"] = "/tmp"

test_user_email = 'test@email.com'

def get_test_user(email = test_user_email):
    return {
        "email": email,
        "token": email
    }

users = [get_test_user(), get_test_user('email2'), get_test_user('email3')]

@mock.patch.dict(os.environ, environ)
class TestDB(TestCase): 

    def setUp(self) -> None:
        from lib.db import Db
        self.db = Db()
        return super().setUp()
        
    def test_db_is_initialized(self):
        self.assertListEqual(self.db.get_users(), [], "Should initialize database")

    def test_add_new_user(self):
        self.db.set_user(get_test_user())
        self.assertListEqual(self.db.get_users(), [get_test_user()], "Should add a new user")

    def test_get_user(self):
        for user in users: 
            self.db.set_user(user)
        self.assertEqual(self.db.get_user("email", 'email2'), get_test_user('email2'), "Should get user from list by attribute")

    def test_get_users(self):
        for user in users: 
            self.db.set_user(user)
        self.assertListEqual(self.db.get_users(), users, 'Should get all the users')
        
    def test_get_user_by_email(self): 
        self.db.set_user(get_test_user())
        self.assertEqual(self.db.get_user_by_email(test_user_email), get_test_user(), 'Should find user by email')
    
    def test_get_user_by_token(self): 
        self.db.set_user(get_test_user())
        self.assertEqual(self.db.get_user_by_token(test_user_email), get_test_user(), 'Should find user by token')
    
    def test_close_database(self):
        self.db.close()
        self.assertTrue(os.path.exists('/tmp/db.json'))
    
    def test_load_exising_database(self): 
        self.db.set_user(get_test_user())
        self.db.close()
        from lib.db import Db
        db = Db()
        self.assertListEqual(self.db.get_users(), db.get_users(), 'Should load an existing database')

    def tearDown(self) -> None:
        try:
            os.remove('/tmp/db.json')
        except: 
            pass
        return super().tearDown()
        
if __name__ == '__main__':
    main()