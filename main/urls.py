from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('question', views.question, name='question'),
    path('signup', views.signup, name='signup'),
    path('tags', views.tags, name='tags')
]


