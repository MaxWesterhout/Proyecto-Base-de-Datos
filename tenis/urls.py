from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('country_best/', views.country_best, name='countrybest'),
	path('latest_result/', views.latest_result, name='latestresult'),
	path('player_tournaments/', views.player_tournaments, name='playertournaments'),
	path('search_players/', views.search_players, name='searchplayers'),
    path('mayo/', views.mayo, name='mayo'),
    path('mayosql/', views.mayosql, name='mayosql'),
    path('mes/', views.mes, name='mes'),
]