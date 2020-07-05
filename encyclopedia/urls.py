from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello/", views.test, name="test"),
    path('search/', views.search),
    #path(r'search/(?P<topic>[^/]+)/$', views.search),
    path('search/<str:topic>', views.search, name="search"),
    path('wiki/<str:subject>', views.wiki, name = "title"),
    path('createNewPage/', views.createNewPage, name= "newPage"),
    path('index/', views.index, name='pageCreated'),
    path('error/', views.index, name='errorPage'),
    path('editPage/<str:subject>', views.editPage, name="edit"),
    path('randomPage/', views.randomPage, name="random")
    
    
    #path('wiki/', views.wiki, name = "title"),
    
    
    #path('random/'),
    #path('new/'),
    #path('edit/')
    
]
