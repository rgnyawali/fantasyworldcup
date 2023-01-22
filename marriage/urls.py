from django.contrib import admin
from django.urls import path
from . import views

app_name = 'marriage'
urlpatterns = [
	path('', views.indexview, name='index'),
	path('gameroom',views.GameView.as_view(), name='gameroom'),
	path('newgame', views.NewGameView.as_view(), name='newgame'),
	path('newplayer', views.NewPlayerView.as_view(), name='newplayer'),

]