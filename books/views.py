from django.shortcuts import render,redirect
from django.views import View
from .models import Book,BookReview,Author
from django.core.paginator import Paginator
from django.views.generic import ListView,TemplateView,DetailView
from .forms import BookReviewForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class BookListView(View):
    def get(self,request):
        books = Book.objects.all().order_by('id')
        
        search_query=request.GET.get('q','')
        if search_query :
            books=books.filter(title__icontains=search_query)
        page_size=request.GET.get('page_size', 4)
        paginator=Paginator(books,page_size)
        page_num=request.GET.get('page',1)
        page_obj=paginator.get_page(page_num)
        
   
        return render(request,
                      'books/list.html',
                      {'page_obj':page_obj, 'search_query':search_query}
                      )

# class BookListView(ListView):
  
#     queryset=Book.objects.all() 
#     context_object_name = 'books'
#     template_name='books/list.html'
#     paginate_by=2
class BookDetailView(View):
    def get(self,request,id):
        book=Book.objects.get(id=id)
        review_form=BookReviewForm()

        return render(request,'books/detail.html',{'book':book,'review_form':review_form})
class AddReviewView(LoginRequiredMixin,View):
    def post(self,request,id):
        book=Book.objects.get(id=id)
        review_form=BookReviewForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                comment=review_form.cleaned_data['comment'],
                stars_given=review_form.cleaned_data['stars_given']
            )
            return redirect(reverse('detail', kwargs={'id':book.id}))
        return render(request,'books/detail.html',{'book':book,'review_form':review_form})
class EditReview(LoginRequiredMixin,View):
    def get(self,request,book_id,review_id):
        book=Book.objects.get(id=book_id)
        review=book.bookreview_set.get(id=review_id)
        review_form=BookReviewForm(instance=review)
        
        return render(request,'books/edit_review.html',{'book':book,'review':review,'review_form':review_form})
    
    def post(self,request,book_id,review_id):
        book=Book.objects.get(id=book_id)
        review=book.bookreview_set.get(id=review_id)
        review_form=BookReviewForm(instance=review,data=request.POST)
        
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('detail', kwargs={'id':book.id}))
        return render(request,'books/edit_review.html',{'book':book,'review':review,'review_form':review_form})

class ConfirmDeleteView(View):
     def get(self,request,book_id,review_id):
        book=Book.objects.get(id=book_id)
        review=book.bookreview_set.get(id=review_id)
         
        return render(request,'books/confirm_delete_review.html',{'book':book,'review':review})
class DeleteReviewView(View):
     def get(self,request,book_id,review_id):
        book=Book.objects.get(id=book_id)
        review=book.bookreview_set.get(id=review_id)
        
        review.delete()
        messages.info(request,'you you have successfuly deleted this review !')
         
        return redirect(reverse('detail',kwargs={'id':book.id}))
    
class AllAuthorsPageView(ListView):
    queryset=Author.objects.all()
    context_object_name='authors'
    template_name='authors/authors.html'
    paginate_by=7
class AuthorDetailView(View):
    
  
    def get(self,request,id):
        author=Author.objects.get(id=id)
        return render(request,'authors/author_detail.html',{'author':author})
        