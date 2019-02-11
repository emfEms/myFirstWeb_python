from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^test/$', views.post_list2, name='post_list2'),
    url(r'^abc/$', views.post_list3, name='post_list3'),
]