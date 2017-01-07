"""Test views."""

# import json
# from operator import itemgetter

# from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client

# from tests.base import BaseTestCase
# from django.test import Client
from django.test import TestCase


class IndexViewTests(TestCase):
    """Test endpoint for views."""

    def setUp(self):
        """Add an http client to test object."""
        super(IndexViewTests, self).setUp()
        self.client = Client()

    def test_index_page(self):
        """Test if index page returns 200."""
        url = reverse('dynamicdecorators-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
