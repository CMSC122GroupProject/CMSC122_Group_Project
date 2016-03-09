from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.dine_query_list, name='dine_query_list'),
    url(r'^restaurants$', views.dine_query_list, name='dine_query_list'),

    #url(r'^$', views.dine_query_algo, name='dine_query_algo'),
    url(r'^query/new/$', views.dine_query_new, name='dine_query_new'),
    url(r'^movies$', views.movies_query_list, name='movies_query_list'),
    url(r'home$', views.main_page, name='home_page')
]