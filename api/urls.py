from django.urls import path
from api.views import  BookReviewApiView,BookReviewListApiView
urlpatterns=[
    path('reviews/',BookReviewListApiView.as_view(),name='reviews_list'),
    path('reviews/<int:id>/',BookReviewApiView.as_view(),name='review_detail'),
    ]