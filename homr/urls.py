from django.urls import path,include
from homr import views
from blog import urls as blog_urls
urlpatterns = [
  path('',include(blog_urls)),
    path('', views.home1,name = 'instant'),
  
    ]