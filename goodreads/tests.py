from django.test import TestCase
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from books.models import Book,BookReview

class HomePageTestCase(TestCase):
    
    def test_home_page(self):
        user = CustomUser.objects.create(username='raxmatjon')
        user.set_password('somepassword')
        user.save()
        book=Book.objects.create(title='book1',description='description1',isbn='123456')
        review0=BookReview.objects.create(user=user,book=book,stars_given=3,comment='quit powerful nice book')
        review1=BookReview.objects.create(user=user,book=book,stars_given=3,comment='nice book')
        review2=BookReview.objects.create(user=user,book=book,stars_given=3,comment='useful book')
        review3=BookReview.objects.create(user=user,book=book,stars_given=3,comment='good book')
     
        response=self.client.get(reverse('home_page')+'?page_size=4')
        
        # self.assertContains(response,review1.comment)
        # self.assertContains(response,review0.comment)
        self.assertContains(response,review2.comment)
        self.assertContains(response,review3.comment)
        self.assertContains(response,review1.comment)
        self.assertContains(response,review0.comment)
        
        
    