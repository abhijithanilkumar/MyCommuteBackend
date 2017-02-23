from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^validate/', views.validate, name='validate'),
]
