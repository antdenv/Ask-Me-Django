from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('hot/', hot, name='hot'),
    path('question/<int:pk>/', question, name='question'),
    path('settings/', settings, name='settings'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('ask/', ask, name='ask'),
    path('tag/<str:tag_name>', tag, name='tag'),
    url(r'^(?P<username>[a-zA-Zа-яА-Я_\-\.0-9]+?)$', profile, name='profile'),
    url(r'^logout/.*?$', logout, name='logout'),
    re_path(r'^/', index),
    url(r'^api/question/(?P<pk>\d+)/like/$',
        login_required(VotesView.as_view(model=Question, vote_type=Like.LIKE)),
        name='question_like'),
    url(r'^api/question/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Question, vote_type=Like.DISLIKE)),
        name='question_dislike'),
    url(r'^status-change/.*', answer_status_change, name="status-change"),
    url(r'^api/answer/(?P<pk>\d+)/like/$',
        login_required(VotesView.as_view(model=Answer, vote_type=Like.LIKE)),
        name='answer_like'),
    url(r'^api/answer/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Answer, vote_type=Like.DISLIKE)),
        name='answer_dislike')
]


