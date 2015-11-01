from django.test import TestCase
from YAASApp.models import Auction
from datetime import datetime
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth
from django.core import mail


# Create your tests here.
class SimpleTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        user = User.objects.create_user('temporaly','temporaly@gmail.com','1234')

    def test_login(self):
        c = Client()
        response = c.post('/yaas/loginuser/', {'username': 'temporaly', 'password': '1234'})

    def test_save(self):
        c = Client()
        c.post('/yaas/loginuser/', {'username': 'temporaly', 'password': '1234'})
        auc_DeadLine = "2015-11-01" +" "+ str(13) +":" + str(11)
        resp = self.client.post('/yaas/saveaucconf/', {'titleAuc':'auc_titleAuc', 'auxDate':auc_DeadLine, 'content':'auc_content', 'minPrice':'23', 'option':'Yes'})
        self.assertEqual(resp.status_code,200)
        self.assertContains(resp,"Thanks.")