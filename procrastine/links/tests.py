"""
Unit test for the links app
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from links.models import Link

class LinksTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='owner',
                                              email='owner@ownership.cc')
        self.url = 'http://google.com/'
        self.link = Link.objects.create(owner=self.owner, url=self.url)
        
    def test_check_if_link_was_created(self):
        """
        Test if the link was created correctly in the setUp method
        """
        self.assertTrue(self.link.id is not None)
        self.assertEquals(self.owner.id, self.link.owner.id)
        self.assertEquals(self.url, self.link.url)

    def test_add_view_post(self):
        """
        Tests adding a URL via POST 
        """
        r = self.client.post(reverse('links_add'), {
            'url': self.url, 'owner': self.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals('Link added', rjson['message'])
        self.assertEquals(2, rjson['link']['id'])
        self.assertEquals(self.url, rjson['link']['url'])

    def test_add_view_get(self):
        """
        Test the response on an invalid request method
        """
        r = self.client.get(reverse('links_add'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])
    
    def test_add_view_empty_post(self):
        """
        Test the response on an empty POST request
        """
        r = self.client.post(reverse('links_add'), {})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])

        self.assertEquals('An error occurred during the link save.', rjson['message'])
    
    def test_add_view_invalid_post(self):
        """
        Test the response on an invalid POST request
        """
        r = self.client.post(reverse('links_add'), {'url': 'http://'})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('An error occurred during the link save.', rjson['message'])

    def test_remove_view_get(self):
        """
        Test invalid request method for the remove view
        """
        r = self.client.get(reverse('links_remove'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])

    def test_remove_view_post(self):
        """
        Test valid post to the remove view
        """
        r = self.client.post(reverse('links_remove'), {
            'id': self.link.id, 'owner': self.link.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(200, rjson['status'])
        self.assertEquals('Link removed', rjson['message'])

        link = Link.objects.get(pk=self.link.id)
        self.assertFalse(link.is_active)

    def test_remove_view_link_not_found(self):
        """
        Test remove view with invalid link id
        """
        r = self.client.post(reverse('links_remove'), {
            'id': 0, 'owner': self.owner.id
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(404, rjson['status'])
        self.assertEquals('Link not found', rjson['message'])

    def test_remove_view_link_not_found(self):
        """
        Test remove view with invalid link owner id
        """
        r = self.client.post(reverse('links_remove'), {
            'id': self.link.id, 'owner': 0 
        })
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(404, rjson['status'])
        self.assertEquals('Link not found', rjson['message'])
    
    def test_list_view(self):
        """
        Test the list view
        """
        r = self.client.post(reverse('links_list'), {'owner': self.owner.id})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(1, len(rjson['urls']))
        self.assertTrue('id' in rjson['urls'][0])
        self.assertTrue('url' in rjson['urls'][0])

    def test_list_view_invalid_post(self):
        """
        Teste the list view with an empty/invalid post
        """
        r = self.client.post(reverse('links_list'), {})
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Owner id not received', rjson['message'])
    
    def test_list_view_get(self):
        """
        Test invalid request method for the listing view
        """
        r = self.client.get(reverse('links_list'))
        self.assertEquals(200, r.status_code)
        rjson = json.loads(r.content)
        self.assertEquals(500, rjson['status'])
        self.assertEquals('Invalid request method', rjson['message'])

    def test_api_key_decorator_valid_call(self):
        """
        Test an valid API key call
        """
        api_key = self.owner.get_profile().key
        r = self.client.get(reverse('api_links_list', args=[api_key]))
        self.assertEquals(200, r.status_code)

    def test_api_key_decorator_invalid_call(self):
        """
        Test an valid API key call
        """
        api_key = 'a' * 40 
        r = self.client.get(reverse('api_links_list', args=[api_key]))
        self.assertEquals(404, r.status_code)

