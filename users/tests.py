from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

# Create your tests here.
class RegistrationTestCase(TestCase):

    def test_CustomUser_account_is_created(self):
        self.client.post(reverse('register'), data={
            'username': 'raxmatjon12',
            'email': 'raxmat@mail.ru',
            'first_name': 'raxmatjon',
            'last_name': 'khamidov',
            'password': 'somepassword'
        })
        user = CustomUser.objects.get(username='raxmatjon12')
        self.assertEqual(user.first_name, 'raxmatjon')
        self.assertEqual(user.last_name, 'khamidov')
        self.assertEqual(user.email, 'raxmat@mail.ru')
        self.assertTrue(user.password, 'somepassword')

    def test_required_fields(self):
        response = self.client.post(reverse('register'),
                                    data={
                                        'email': 'salo@mail.ru',
                                        'first_name': 'raxmatjon'
                                    })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_email_is_valid(self):
        response = self.client.post(reverse('register'), data={
            'username': 'raxmatjon12',
            'email': 'invalid-email',
            'first_name': 'raxmatjon',
            'last_name': 'khamidov',
            'password': 'somepassword'
        })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_username_is_unique(self):
        user = CustomUser.objects.create(username='raxmatjon')
        user.set_password('somepassword')
        user.save()
        response = self.client.post(reverse('register'), data={
            'username': 'raxmatjon',

            'first_name': 'raxmatjon',
            'last_name': 'khamidov',
            'password': 'somepassword'
        })
        user_count=CustomUser.objects.count()
        self.assertEqual(user_count,1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')



class LoginTestCase(TestCase):

    def setUp(self):
        self.CustomUser_db = CustomUser.objects.create(username='raxmatjon')
        self.CustomUser_db.set_password('somepassword')
        self.CustomUser_db.save()
    def test_CustomUser_successfull_logged_in(self):

        self.client.post(reverse('login'),
                         data={
                             'username':'raxmatjon',
                             'password':'somepassword'


                         })
        user=get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_CustomUser_wrong_credentials(self):

        self.client.post(reverse('login'),
                         data={
                             'username': 'wrong-raxmatjon',
                             'password': 'somepassword'
                         }
                         )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.client.post(reverse('login'),
                         data={
                             'username': 'raxmatjon',
                             'password': 'wrong-somepassword'
                         }
                         )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
    def test_CustomUser_logout(self):
        self.client.login(username='raxmatjon',password='somepassword')
        self.client.get(reverse('logout'))
        user=get_user(self.client)
    
        self.assertFalse(user.is_authenticated)
class ProfileTestCase(TestCase):
    def test_login_required(self):
       response= self.client.get(reverse('profile'))
       self.assertEqual(response.status_code,302)
    #    self.assertEqual(response.url,reverse('login')+'?next=/users/profile/')

    def test_profile_details(self):
        user=CustomUser.objects.create(username='raxmatjon',first_name='raxmatjon',last_name='hamidov')
        user.set_password('password')
        user.save()

        self.client.login(username='raxmatjon',password='password')
        response=self.client.get(reverse('profile'))

        self.assertContains(response,user.username)
        self.assertContains(response,user.first_name)
        self.assertContains(response,user.last_name)
    
    def test_update_profile(self):
        user=CustomUser.objects.create(username='raxmatjon',first_name='raxmatjon',last_name='hamidov')
        user.set_password('password')
        user.save()
        self.client.login(username='raxmatjon',password='password')
        response=self.client.post(
            reverse('profile_update'),
            data={
                'username':'raxmatjon',
                
                'last_name':'lastname'
            })
        user=CustomUser.objects.get(pk=user.pk) #or user.refresh_from_db
        self.assertEqual(user.last_name,'lastname')
        self.assertEqual(response.url,reverse('profile'))
        