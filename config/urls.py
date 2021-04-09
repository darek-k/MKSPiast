"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import SignIn, Logout, SignUp
from core.views import IndexView, blog, contact, news, ArticleDetailView, team, AddCommentView, AdminListView, \
    AdminArticlesView, AdminTeamsView, AdminMatchesView, AdminMatchweeksView, AddArticleView, AddMatchWeekView, \
    AddTeamView, AddMatchView, EditArticleView, EditTeamView, EditMatchView, EditMatchWeekView, DeleteArticleView, \
    DeleteTeamView, DeleteMatchView, DeleteMatchWeekView, AdminPlayersView, AddPlayerView, EditPlayerView, \
    DeletePlayerView, about, base, DeleteNextMatchWeekView, AdminNextMatchWeekView, AddNextMatchWeekView, \
    EditNextMatchWeekView, DownloadTeams, DownloadMatches
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('article_detail/<pk>/', ArticleDetailView.as_view(), name='article_detail'),

    path('admin_view/', AdminListView.as_view(), name='admin_list'),
    path('admin_articles/', AdminArticlesView.as_view(), name='admin_articles'),
    path('admin_teams/', AdminTeamsView.as_view(), name='admin_teams'),
    path('admin_matches/', AdminMatchesView.as_view(), name='admin_matches'),
    path('admin_matchweeks/', AdminMatchweeksView.as_view(), name='admin_matchweeks'),
    path('admin_next_matchweek/', AdminNextMatchWeekView.as_view(), name='admin_next_matchweek'),
    path('admin_players/', AdminPlayersView.as_view(), name='admin_players'),

    path('article/<pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('admin_articles/add_article/', AddArticleView.as_view(), name='add_article'),
    path('admin_teams/add_team/', AddTeamView.as_view(), name='add_team'),
    path('admin_matches/add_match/', AddMatchView.as_view(), name='add_match'),
    path('admin_matchweeks/add_matchweek/', AddMatchWeekView.as_view(), name='add_matchweek'),
    path('admin_next_matchweek/add_next_matchweek/', AddNextMatchWeekView.as_view(), name='add_next_matchweek'),
    path('admin_players/add_player/', AddPlayerView.as_view(), name='add_player'),

    path('admin_articles/edit_article/<pk>/', EditArticleView.as_view(), name='edit_article'),
    path('admin_teams/edit_team/<pk>/', EditTeamView.as_view(), name='edit_team'),
    path('admin_matches/edit_match/<pk>/', EditMatchView.as_view(), name='edit_match'),
    path('admin_matchweeks/edit_matchweek/<pk>/', EditMatchWeekView.as_view(), name='edit_matchweek'),
    path('admin_next_matchweek/edit_next_matchweek/<pk>/', EditNextMatchWeekView.as_view(), name='edit_next_matchweek'),
    path('admin_players/edit_player/<pk>/', EditPlayerView.as_view(), name='edit_player'),

    path('admin_articles/delete_article/<pk>/', DeleteArticleView.as_view(), name='delete_article'),
    path('admin_teams/delete_team/<pk>/', DeleteTeamView.as_view(), name='delete_team'),
    path('admin_matches/delete_match/<pk>/', DeleteMatchView.as_view(), name='delete_match'),
    path('admin_matchweeks/delete_matchweek/<pk>/', DeleteMatchWeekView.as_view(), name='delete_matchweek'),
    path('admin_next_matchweek/delete_next_matchweek/<pk>/', DeleteNextMatchWeekView.as_view(),
         name='delete_next_matchweek'),
    path('admin_players/delete_player/<pk>/', DeletePlayerView.as_view(), name='delete_player'),

    path('admin_teams/team_download/', DownloadTeams.as_view(), name='team_download'),
    path('admin_matches/automatic_match_download/', DownloadMatches.as_view(), name='automatic_match_download'),

    path('register/', SignUp.as_view(), name='register'),
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('blog/', blog, name='blog'),
    path('base/', base, name='base'),
    path('contact/', contact, name='contact'),
    path('news/', news, name='news'),
    path('team/', team, name='team'),
    path('about/', about, name='about'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
