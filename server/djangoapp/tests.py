import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel

class AuthenticationAndReviewTests(TestCase):
    def setUp(self):
        self.client=Client(enforce_csrf_checks=True)
        self.user=User.objects.create_user('testreviewer',password='Demo-password-294!')
        make=CarMake.objects.create(name='Test Make')
        self.car=CarModel.objects.create(car_make=make,name='Test Model',type='Sedan',year=2023)
    def post(self,path,data):
        csrf=self.client.get('/djangoapp/csrf').json()['csrfToken']
        return self.client.post('/djangoapp/'+path,json.dumps(data),content_type='application/json',HTTP_X_CSRFTOKEN=csrf)
    def test_csrf_and_login_lifecycle(self):
        self.assertEqual(self.client.post('/djangoapp/login','{}',content_type='application/json').status_code,403)
        self.assertEqual(self.post('login',{'userName':'testreviewer','password':'wrong'}).status_code,401)
        self.assertEqual(self.post('login',{'userName':'testreviewer','password':'Demo-password-294!'}).status_code,200)
        self.assertEqual(self.client.get('/djangoapp/session').json()['userName'],'testreviewer')
        self.post('logout',{})
        self.assertIsNone(self.client.get('/djangoapp/session').json()['userName'])
    def test_registration_rejects_duplicate_username(self):
        result=self.post('register',{'userName':'testreviewer','password':'Other-password-782!'})
        self.assertEqual(result.status_code,409)
        self.assertEqual(User.objects.count(),1)
    def test_unauthenticated_review_is_rejected(self):
        self.assertEqual(self.post('add_review',{}).status_code,401)
    @patch('djangoapp.views.post_review',return_value={'id':101})
    def test_review_uses_authenticated_identity_and_valid_car(self,remote):
        self.client.force_login(self.user)
        data={'car_id':self.car.pk,'dealership':1,'review':'Demo review','purchase_date':'2023-01-01','name':'Spoofed'}
        self.assertEqual(self.post('add_review',data).status_code,201)
        self.assertEqual(remote.call_args.args[0]['name'],'testreviewer')
        self.assertEqual(remote.call_args.args[0]['car_make'],'Test Make')
        data['car_id']=9999
        self.assertEqual(self.post('add_review',data).status_code,400)
