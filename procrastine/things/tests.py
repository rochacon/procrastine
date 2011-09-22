"""
Unit test for the things app
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from things.forms import ThingForm 
from things.models import Thing 

class ThingTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='owner',
                                              email='owner@ownership.cc')
        self.types = dict((k, v) for v, k in Thing.TYPES)
        self.content = {
            'url': 'http://google.com/'
        }
        self.thing_url = Thing.objects.create(
            owner=self.owner,
            content=self.content['url'],
            type=self.types['url']
        )
        
    def test_check_if_thing_url_was_created(self):
        """
        Test if the thing was created correctly in the setUp method
        """
        self.assertTrue(self.thing_url.id is not None)
        self.assertEquals(self.owner.id, self.thing_url.owner.id)
        self.assertEquals(self.content['url'], self.thing_url.content)
        self.assertEquals(self.types['url'], self.thing_url.type)

    def test_add_url_view_post(self):
        """
        Tests adding a URL via POST 
        """
        r = self.client.post(reverse('things_add'), {
            'content': self.content['url'], 'owner': self.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals('Added', rjson['message'])
        self.assertEquals(2, rjson['thing']['id'])
        self.assertEquals(self.content['url'], rjson['thing']['content'])
        self.assertEquals('url', rjson['thing']['type'])
        thing = Thing.objects.get(pk=rjson['thing']['id'])
        self.assertEquals(True, thing.is_active)

    def test_add_view_get(self):
        """
        Test the response on an invalid request method
        """
        r = self.client.get(reverse('things_add'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])
    
    def test_add_view_empty_post(self):
        """
        Test the response on an empty POST request
        """
        r = self.client.post(reverse('things_add'), {})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])

        self.assertEquals('An error occurred during the save process.', rjson['message'])
    
    def test_add_view_invalid_post(self):
        """
        Test the response on an invalid POST request
        """
        r = self.client.post(reverse('things_add'), {'url': 'http://'})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('An error occurred during the save process.', rjson['message'])

    def test_remove_view_get(self):
        """
        Test invalid request method for the remove view
        """
        r = self.client.get(reverse('things_remove'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])

    def test_remove_view_post(self):
        """
        Test valid post to the remove view
        """
        r = self.client.post(reverse('things_remove'), {
            'id': self.thing_url.id, 'owner': self.thing_url.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(200, rjson['status'])
        self.assertEquals('Removed', rjson['message'])

        thing = Thing.objects.get(pk=self.thing_url.id)
        self.assertFalse(thing.is_active)

    def test_remove_view_thing_not_found(self):
        """
        Test remove view with invalid thing id
        """
        r = self.client.post(reverse('things_remove'), {
            'id': 0, 'owner': self.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(404, rjson['status'])
        self.assertEquals('Not found', rjson['message'])
    
    def test_list_view(self):
        """
        Test the list view
        """
        r = self.client.post(reverse('things_list'), {'owner': self.owner.id})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(1, len(rjson['things']))
        self.assertTrue('id' in rjson['things'][0])
        self.assertTrue('content' in rjson['things'][0])
        self.assertTrue('type' in rjson['things'][0])
        self.assertTrue('url' in rjson['things'][0])

    def test_list_view_invalid_post(self):
        """
        Teste the list view with an empty/invalid post
        """
        r = self.client.post(reverse('things_list'), {})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Owner id not received', rjson['message'])
    
    def test_list_view_get(self):
        """
        Test invalid request method for the listing view
        """
        r = self.client.get(reverse('things_list'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])

    def test_api_key_decorator_valid_call(self):
        """
        Test an valid API key call
        """
        api_key = self.owner.get_profile().key
        r = self.client.get(reverse('api_things_list', args=[api_key]))
        self.assertEquals(200, r.status_code)

    def test_api_key_decorator_invalid_call(self):
        """
        Test an valid API key call
        """
        api_key = 'a' * 40 
        r = self.client.get(reverse('api_things_list', args=[api_key]))
        self.assertEquals(404, r.status_code)

    def test_form_clean_type(self):
        """
        Test if the ThingForm clean is working properly
        """
        form = ThingForm({'content': self.content['url'], 'owner': self.owner.id})
        self.assertEquals({}, form.errors)
        self.assertEquals(self.types['url'], form.cleaned_data['type'])

        # TODO test type image
        # TODO test type text

