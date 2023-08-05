from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.
from books.models import Book, BookAuthor,BookReview
from users.models import CustomUser
from rest_framework.reverse import reverse
class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="raxmatjon", first_name="raxmatjon")
        self.user.set_password("somepass")
        self.user.save()
        
        self.client.login(username='raxmatjon',password='somepass')
        
    
    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.get(reverse('review_detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], '123121')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], "raxmatjon")
        self.assertEqual(response.data['user']['username'], "raxmatjon")
    
    
    def test_book_reviewdelete(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.delete(reverse('review_detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code,204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())
        
    def test_bookreview_patch(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.patch(reverse('review_detail', kwargs={'id': br.id}),data={'stars_given':3})
        br.refresh_from_db()
        
        self.assertEqual(br.stars_given,3)
        
    def test_bookreview_put(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.put(reverse('review_detail', 
                                             kwargs={'id': br.id}),
                                     data={'stars_given':4,
                                           'comment':'nice',
                                           'user_id':self.user.id,
                                           'book_id':book.id})
        br.refresh_from_db()
        
        self.assertEqual(br.stars_given,4)
        self.assertEqual(br.comment,'nice')
        
        
    
    def test_book_review_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        
        response = self.client.post(reverse('reviews_list', 
                                             ),
                                     data={'stars_given':4,
                                           'comment':'nice',
                                           'user_id':self.user.id,
                                           'book_id':book.id})
        
        br=BookReview.objects.get(book=book)
        
        self.assertEqual(response.status_code,201)
        self.assertEqual(br.comment,'nice')
        self.assertEqual(br.stars_given,4)
        
        