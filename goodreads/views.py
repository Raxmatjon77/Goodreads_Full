from django.http import HttpResponse
from django.shortcuts import render
from books.models import BookReview,Book
from django.core.paginator import Paginator
import random
from django.views import View
# def landing_page(request):
 
class landingPageView(View):
    def get(self,request):
        recommended_books=Book.objects.all()[0]
        context={
            'books':recommended_books
        }
        return render(request,'landing.html',context)

def home_page(request):
    book_reviews=BookReview.objects.all().order_by('-created_at')
    page_size=request.GET.get('page_size', 2)
    paginator=Paginator(book_reviews,page_size)
    page_num=request.GET.get('page',1)
    page_obj=paginator.get_page(page_num)
    
    return render(request,'home.html',{'page_obj':page_obj})