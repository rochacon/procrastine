import random
import string

from django.test import TestCase
from django.contrib.auth.models import User

class AccountsTest(TestCase):
    def test_hash_generation(self):
        """
        Tests that a hash is created for the newly created user 
        """
        u = {'username': 'test', 'email': 'test@test.cc', 'password': 'test'}
        user = User.objects.create_user(**u)
        self.assertTrue(user.id is not None)
        self.assertTrue(40, len(user.get_profile().key)) # SHA-1 hash key


def ProfileTestCase(TestCase):
    """
    Test account 
    """
    def test_profile_view_anon(self):
        """
        Test if profile view link is authentication proof
        """
        url = reverse('accounts_profile')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('index'))

    # TODO
    # Profile view test
