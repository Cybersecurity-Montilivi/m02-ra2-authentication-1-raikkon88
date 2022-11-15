import sys
import os
from unittest import TestCase, mock, main
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


environ = os.environ
environ["VOLUME_PATH"] = "./tmp"


@mock.patch.dict(os.environ, environ)
class TestRegister(TestCase):

    def setUp(self):
        from lib.users import Users
        from lib.db import Db
        db = Db()
        self.users = Users(db)
        return super().setUp()

    def test_register_generate_token(self):
        email = 'fake@email.com'
        user = self.users.register(email)
        self.assertEqual(user['email'], email,
                         'Should have initialized the proper email')
        self.assertIsNotNone(user['token'], 'Should have token assigned')

    def test_register_token_is_strong_enough(self):
        user = self.users.register('fake@email.com')
        self.assertGreater(len(user['token']), 64,
                           'The token is strong enogth')

    def test_register_user_exists(self):
        try:
            self.users.register('fake@email.com')
            self.users.register('fake@email.com')
        except Exception as err:
            self.assertEqual(str(err), "The user already exists",
                             'Should not register the same user twice')


if __name__ == '__main__':
    main()
