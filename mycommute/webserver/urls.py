from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^buslogin/', views.buslogin, name='buslogin'),
    url(r'^readqr/', views.readqr, name='readqr'),
    url(r'^login/', views.login, name='login'),
]
