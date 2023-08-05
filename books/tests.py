from django.test import TestCase
from django.urls import reverse

from books.models import Book,BookAuthor,Author
from users.models import CustomUser

# Create your tests here.
class BookTestCase(TestCase):

    def test_no_books(self):
        response=self.client.get(reverse('book_list'))

        self.assertContains(response,'no books found')
    def test_book_list(self):
        book1=Book.objects.create(title='book1',description='description1',isbn='123456')
        book2=Book.objects.create(title='book2',description='description2',isbn='12345333')
        book3=Book.objects.create(title='book3',description='description3',isbn='1234533')
        response=self.client.get(reverse('book_list'))
        books=Book.objects.all()

        for book in [book1,book2 ,book3]:
            self.assertContains(response,book.title)
        
    def test_detail_page(self):
        book=Book.objects.create(title='book1',description='description1',isbn='123456')
        response=self.client.get(reverse('detail',kwargs={'id':book.id}))

        self.assertContains(response,book.title)
        self.assertContains(response,book.description)
        
    def test_search_book(self):
        
        book1=Book.objects.create(title='book1',description='description1',isbn='123456')
        book2=Book.objects.create(title='book2',description='description2',isbn='12345333')
        book3=Book.objects.create(title='book3',description='description3',isbn='1234533')
        response=self.client.get(reverse('book_list')+'?q=book1')
        self.assertNotContains(response,book3.title)
        self.assertNotContains(response,book2.title)
        self.assertContains(response,book1.title)
        
        response=self.client.get(reverse('book_list')+'?q=book3')
        self.assertNotContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertContains(response,book3.title)
        
        response=self.client.get(reverse('book_list')+'?q=book2')
        self.assertNotContains(response,book3.title)
        self.assertNotContains(response,book1.title)
        self.assertContains(response,book2.title)
        
class AddReviewTestCase(TestCase):
    
    def test_add_review(self):
        book=Book.objects.create(title='book1',description='description1',isbn='123456')
        user=CustomUser.objects.create(username='raxmatjon',first_name='raxmatjon',last_name='hamidov')
        user.set_password('password')
        user.save()

        self.client.login(username='raxmatjon',password='password')
        
        self.client.post(reverse('reviews', kwargs={'id':book.id}),
                         data={'stars_given':3,
                               'comment':'nice book'}
                         )
        book_reviews=book.bookreview_set.all()
        self.assertEqual(book_reviews.count(),1)
        self.assertEqual(book_reviews[0].user,user)
        self.assertEqual(book_reviews[0].book,book)
        self.assertEqual(book_reviews[0].comment,'nice book')
        self.assertEqual(book_reviews[0].stars_given,3)
        
    def test_book_author(self):
        author=Author.objects.create(first_name='raxmatjon',last_name='hamidov',email='email@mail.com',bio='bio')
        book=Book.objects.create(title='book1',description='description1',isbn='123456')
        book_author=BookAuthor.objects.create(book=book,author=author)
        response=self.client.get(reverse('detail',kwargs={'id':book.id}))
        
        self.assertContains(response,book_author.author.first_name)
        self.assertContains(response,book_author.author.last_name)
        
 