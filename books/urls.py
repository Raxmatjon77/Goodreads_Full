from django.urls import path

from books.views import BookListView, BookDetailView,AddReviewView,EditReview,ConfirmDeleteView,DeleteReviewView,\
AllAuthorsPageView,AuthorDetailView
urlpatterns=[
    path('',BookListView.as_view(),name='book_list'),
    path('<int:id>/',BookDetailView.as_view(),name='detail'),
    path('<int:id>/reviews/',AddReviewView.as_view(),name='reviews'),
    path('<int:book_id>/reviews/<int:review_id>/edit/',EditReview.as_view(),name='edit_review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/confirm/',ConfirmDeleteView.as_view(),name='delete_confirm'),
    path('<int:book_id>/reviews/<int:review_id>/delete/',DeleteReviewView.as_view(),name='delete_review'),
    path('authors/',AllAuthorsPageView.as_view(),name='authors'),
    path('authors/<int:id>/',AuthorDetailView.as_view(),name='author_detail')
]