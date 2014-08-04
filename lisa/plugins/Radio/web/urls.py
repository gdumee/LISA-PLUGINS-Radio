from django.conf.urls import patterns, url
from lisa.plugins.Radio.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
