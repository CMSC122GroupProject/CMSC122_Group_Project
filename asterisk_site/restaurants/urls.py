from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dine_query_list, name='dine_query_list'),
    url(r'^dine_query/new/$', views.dine_query_new, name='dine_query_new')
]