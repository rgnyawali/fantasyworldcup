from django.urls import path, include
from . import views

app_name = 'tt'
urlpatterns = [
    path('', views.HomeView.as_view(), name='tt_index'),
    path('tt/detail', views.MatchDetailView.as_view(), name='tt_detail'),
    #path('tt/<int:pk>/', views.MatchDetailView.as_view(), name='tt_detail'),
    path('trial/',views.TrialView.as_view(),name='tt_trial'),
    path('admin/', views.AdminView.as_view(), name='admin'),
    ]

