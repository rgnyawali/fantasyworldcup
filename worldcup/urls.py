from django.urls import path, include
from . import views

app_name = 'worldcup'
urlpatterns = [
    #path('', views.HomeView.as_view(), name='homepage'),
    path('register/', views.register_user, name='register'),
    path('', views.IndexView.as_view(), name='worldcup_index'),
    path('prediction/', views.PredictionView.as_view(), name='prediction'),
    #path('knockout/', views.KnockOutPredictionView.as_view(), name='knockout_team_prediction'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('adminUpdate/', views.AdminUpdateView.as_view(), name='admin_update'),
    path('quarterUpdate/', views.QuarterFinalUpdateView.as_view(), name='quarter_update'),
    path('semiUpdate/', views.SemiFinalUpdateView.as_view(), name='semi_update'),
    path('finalUpdate/', views.FinalUpdateView.as_view(), name='final_update'),
    path('champUpdate/', views.ChampUpdateView.as_view(), name='champ_update'),
    path('rules/', views.rules, name='rules'),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    ]

