from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='home'
urlpatterns = [
    path('',views.HomeView.as_view(), name='index'),
    #path('register/', views.register_user, name="register"), #Need to uncomment after register_user view is created

    ]