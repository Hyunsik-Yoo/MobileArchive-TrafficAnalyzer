from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^index/$', views.index, name='index'),
    url(r'^app', views.selection_app, name='selection_app'),
    url(r'^index/name/$', views.after_selection_app, name='after_selection_app'),
    url(r'^run/$', views.run_test, name='run_test')
]
