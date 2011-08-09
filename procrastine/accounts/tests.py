import random
import string

from django.test import TestCase
from django.contrib.auth.models import User

class AccountTest(TestCase):
    def test_hash_generation(self):
        """
        Tests that a hash is created for the newly created user 
        """
        u = {'username': 'test', 'email': 'test@test.cc', 'password': 'test'}
        u['key'] = ''.join(random.choice(string.letters + string.digits) for x in range(0,40))
        user = User.objects.create_user(**u)
        self.assertTrue(user.id is not None)
        self.assertTrue(40, len(user.get_profile().key)) # SHA-1 hash key
