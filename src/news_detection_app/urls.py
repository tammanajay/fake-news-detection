from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('upload/', upload, name='upload'),
    path('article_list/', article_list, name='article_list'),
    path("articles/<int:article_id>/", article_detail, name="article_detail"),
]
