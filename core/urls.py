from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms, name='rooms'),
    path('gallery/', views.gallery, name='gallery'),
    path('inquiry/', views.inquiry, name='inquiry'),
]
