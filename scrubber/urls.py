from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'saveScrub$', views.doScrub),
    url(r'getTask$', views.getTask),
    url(r'getHit$', views.getHit),
]
