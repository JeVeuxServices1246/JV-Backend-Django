from django.test import TestCase

from login.models import User, UserRole

from login.views import (
    generate_token,
    generate_user_data
)

class TestUtils(TestCase):

    def setUp(self):
        self.user_role_obj = UserRole.objects.create(name='user')
        self.user_obj = User.objects.create(
            country_code=1, phone_number='1234567890', first_name='S', last_name='P',
            email='sp@test.com', username='sp', role=self.user_role_obj)

    def test_generate_user_data(self):
        user_obj = self.user_obj
        user_data = generate_user_data(user_obj)
        self.assertEqual(user_data['user_id'], user_obj.id)
        self.assertEqual(user_data['country_code'], user_obj.country_code)
        self.assertEqual(user_data['phone_number'], user_obj.phone_number)
        self.assertEqual(user_data['username'], user_obj.username)
        self.assertEqual(user_data['first_name'], user_obj.first_name)
        self.assertEqual(user_data['last_name'], user_obj.last_name)
        self.assertEqual(user_data['email'], user_obj.email)
        self.assertEqual(user_data['profile_pic'], user_obj.profile_pic)
        self.assertEqual(user_data['email_verified'], user_obj.email_verified)

    def test_generate_token(self):
        user_obj = self.user_obj
        user_data = generate_user_data(user_obj)
        token = generate_token(user_data, login_type='app')
        self.assertIsNotNone(token)