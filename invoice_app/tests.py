from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

# Create your tests here.
class EntrepPageTest(SimpleTestCase):
    def test_entrepView_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        
    def test_entrepView_url_code(self):
        response = self.client.get(reverse('add-entrepreneur'))
        self.assertEqual(response.status_code, 302)