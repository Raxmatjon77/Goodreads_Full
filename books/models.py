from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    cover_picture=models.ImageField(default='cover_book.jpg')
    isbn=models.CharField(max_length=17)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    bio=models.TextField()
    author_cover_picture=models.ImageField(default='author_cover_pic.jpg')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class BookAuthor(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        
        return f"{self.book.title} by {self.author.first_name}"



class BookReview(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)
    stars_given=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return f"{self.stars_given} stars  by {self.user.username} for {self.book.title}"
