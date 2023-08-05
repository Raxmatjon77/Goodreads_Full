from django.http import HttpResponse
from django.shortcuts import render
from books.models import BookReview
from django.core.paginator import Paginator
import random
def landing_page(request):
    images = [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/The_Lord_of_the_Rings_book_cover.jpg/220px-The_Lord_of_the_Rings_book_cover.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/To_Kill_a_Mockingbird_book_cover.jpg/220px-To_Kill_a_Mockingbird_book_cover.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/The_Great_Gatsby_book_cover.jpg/220px-The_Great_Gatsby_book_cover.jpg',
    ]

    book_image = random.choice(images)

    return render(request,'landing.html',{'book_image':book_image})

def home_page(request):
    book_reviews=BookReview.objects.all().order_by('-created_at')
    page_size=request.GET.get('page_size', 2)
    paginator=Paginator(book_reviews,page_size)
    page_num=request.GET.get('page',1)
    page_obj=paginator.get_page(page_num)
    
    return render(request,'home.html',{'page_obj':page_obj})