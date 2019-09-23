import unittest
import user as user_api
import contact_detail as contact_detail_api
import utils
from random import randint


class TestUser(unittest.TestCase):
    '''
    Presents few sample unit tests for API functions.
    '''

    def test_read_all(self):
        data = user_api.read_all()
        self.assertTrue(len(data) > 0)

    def test_get_by_id(self):
        user = user_api.read_all()[0]
        user_id = user.get('user_id')
        user = user_api.get_by_id(user_id)
        self.assertEqual(user.get('user_id'), user_id)

    def test_create_contact_detail(self):
        user = user_api.read_all()[0]
        contact_detail = {
            'email': f'{user.get("username")}@{utils.generate_random_string(6)}.com'
        }
        result, status = contact_detail_api.create(user.get('user_id'), contact_detail)
        self.assertEqual(status, 201)

    def test_create_user(self):
        # generate random user name as duplicates raise an error
        name = utils.get_random_name()
        surname = utils.get_random_surname()
        username = f'{name[:1]}{surname}'
        new_user = {
            'username': username,
            'first_name': name,
            'surname': surname
        }
        user, status = user_api.create(new_user)
        self.assertEqual(status, 201)

        email = f'{username}@{utils.generate_random_string(6)}.com'
        print(f'creating new email: {email}')
        contact_detail = {
            'email': email
        }
        result, status = contact_detail_api.create(user.get('user_id'), contact_detail)
        assert (status == 201)

    def test_delete_user(self):
        users = user_api.read_all()
        user = users[randint(0, len(users))]
        try:
            user_api.delete(user.get('user_id'))
        except Exception as e:
            self.assertTrue('Working outside of application context' in str(e))

    def test_update_user(self):
        # get existing User
        user = user_api.read_all()[0]

        # update username
        user['username'] = utils.generate_random_string(10)

        # do not update contact details
        del user['contact_details']
        data, status = user_api.update(user.get('user_id'), user)
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()
