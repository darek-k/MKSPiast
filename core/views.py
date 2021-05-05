import math
from datetime import datetime, timezone
import random

import requests
from bs4 import BeautifulSoup
from core.forms import CommentForm, ArticleForm, MatchWeekForm, MatchForm, TeamForm, PlayerForm, NextMatchWeekForm
from core.models import Article, Comment, Team, Match, MatchWeek, Player, NextMatchWeek, MatchTest
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


def club(request):
    return render(request, 'core/club.html')


def base(request):
    return render(request, 'core/base.html')


def blog(request):
    return render(request, 'core/blog.html')


def contact(request):
    return render(request, 'core/contact.html')


def news(request):
    return render(request, 'core/news.html')


""" Detail Views """


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments_number'] = \
            len([comment for comment in Article.objects.get(pk=self.kwargs.get('pk')).comments.all()])
        context['form'] = CommentForm()
        context['teams'] = Team.objects.all()
        context['all_matches'] = Match.objects.all()
        context['matches_test'] = MatchTest.objects.all()

        for match in MatchTest.objects.all():
            if match.home_team_goals == ' -':
                context['next_match_week'] = match.match_week

        return context


""" List Views """


class IndexView(ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        DownloadTeams().update_team_objects(DownloadTeams().download_teams())
        DownloadMatches().create_match_objects(DownloadMatches().download_matches())
        DownloadPlayers().create_players_objects(DownloadPlayers().download_players())

    model = Article
    template_name = 'core/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['articles_3'] = Article.objects.all()[:3]

        if Article.objects.all():
            context['latest_article'] = Article.objects.latest('published_date')
        context['teams'] = Team.objects.all()
        context['all_matches'] = Match.objects.all()
        context['matches_test'] = MatchTest.objects.all()
        context['players_random_4'] = random.sample(list(Player.objects.all()), 4)

        for match in MatchTest.objects.all():
            if match.home_team_goals == ' -':
                context['next_match_week'] = match.match_week

        context['piast_next_match'] = MatchTest.objects.filter(match_week=context['next_match_week']).filter \
            (Q(home_team='Piast Człuchów') | Q(away_team='Piast Człuchów'))

        # next match counting
        for check in context['piast_next_match']:

            if context['piast_next_match'].first().date < datetime.now(timezone.utc):
                context['days'] = 'Rozgrywki zawieszone'
            else:
                context['piast_next_match_date'] = context['piast_next_match'].first().date
                context['result'] = check.date - datetime.now(timezone.utc)
                days = context['result'].days
                hours = math.floor(context['result'].seconds / 3600)
                minutes = (context['result'].seconds // 60) % 60

                if days == 1:
                    context['days'] = f'{days} Dzień'
                else:
                    context['days'] = f'{days} Dni'

                if hours == 1:
                    context['hours'] = f'{hours} Godzina'
                elif hours in (2, 3, 4, 22, 23, 24):
                    context['hours'] = f'{hours} Godziny'
                else:
                    context['hours'] = f'{hours} Godzin'

                if minutes == 1:
                    context['minutes'] = f'{minutes} Minuta'
                elif minutes in (2, 3, 4, 22, 23, 24):
                    context['minutes'] = f'{minutes} Minuty'
                else:
                    context['minutes'] = f'{minutes} Minut'

        return context


class PlayersView(ListView):
    model = Player
    template_name = 'core/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['players'] = Player.objects.all()
        return context


class AdminListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_view.html'
    model = Match

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['teams'] = Team.objects.all()
        context['matches'] = Match.objects.all()
        context['articles'] = Article.objects.all()
        context['comment'] = Comment.objects.all()
        context['matchweek'] = MatchWeek.objects.all()
        return context


class AdminTeamsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_teams.html'
    model = Team

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['teams'] = Team.objects.all()
        return context


class AdminArticlesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_articles.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['articles'] = Article.objects.all()
        return context


class AdminMatchesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_matches.html'
    model = Match

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['matches'] = Match.objects.all()
        return context


class AdminMatchweeksView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_matchweeks.html'
    model = MatchWeek

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['matchweeks'] = MatchWeek.objects.all()
        return context


class AdminNextMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_next_matchweek.html'
    model = NextMatchWeek

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['next_matchweek'] = NextMatchWeek.objects.all()
        return context


class AdminPlayersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    template_name = 'core/admin_players.html'
    model = Player

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['players'] = Player.objects.all()
        return context


"""Create Views"""


class AddCommentView(CreateView):
    model = Comment
    template_name = 'core/article_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        article_id = self.kwargs['pk']
        return reverse_lazy('article_detail', kwargs={'pk': article_id})


class AddArticleView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add article'
    template_name = 'core/form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('admin_articles')


class AddTeamView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add team'
    template_name = 'core/form.html'
    form_class = TeamForm
    success_url = reverse_lazy('admin_teams')


class AddMatchView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add match'
    template_name = 'core/form.html'
    form_class = MatchForm
    success_url = reverse_lazy('admin_matches')


class AddMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add matchweek'
    template_name = 'core/form.html'
    form_class = MatchWeekForm
    success_url = reverse_lazy('admin_matchweeks')


class AddNextMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add next matchweek'
    template_name = 'core/form.html'
    form_class = NextMatchWeekForm
    success_url = reverse_lazy('admin_next_matchweek')


class AddPlayerView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    title = 'Add player'
    template_name = 'core/form.html'
    form_class = PlayerForm
    success_url = reverse_lazy('admin_players')


""" Update Views """


class EditArticleView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Article
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_articles')


class EditTeamView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Team
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_teams')


class EditMatchView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Match
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_matches')


class EditMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = MatchWeek
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_matchweeks')


class EditNextMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = NextMatchWeek
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_next_matchweek')


class EditPlayerView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Player
    fields = '__all__'
    template_name = 'core/form.html'
    success_url = reverse_lazy('admin_players')


""" Delete Views """


class DeleteArticleView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Article
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_articles')


class DeleteTeamView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Team
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_teams')


class DeleteMatchView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Match
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_matches')


class DeleteMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = MatchWeek
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_matchweeks')


class DeleteNextMatchWeekView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = NextMatchWeek
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_next_matchweek')


class DeletePlayerView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'user.is_staff'
    permission_denied_message = 'Tylko dla upoważnionych użytkowników'

    model = Player
    template_name = 'core/delete_form.html'
    success_url = reverse_lazy('admin_players')


""" Web Scrapping """


def take_soup(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


class DownloadTeams(TemplateView):
    def __init__(self):
        if Team.objects.all().count() != 20:
            self.create_team_objects(self.download_teams())

    template_name = 'core/admin_teams.html'

    def download_teams(self):
        table = take_soup('http://www.pomorskifutbol.pl/liga.php?id=1309').find('table', class_='tabela')
        rows = table.find_all('tr')[2:]
        proper_number_of_rows = 14

        team_dict = {}
        for row in rows:
            cells = row.find_all('td')

            if len(cells) == proper_number_of_rows:
                club_name = cells[1].text.strip()
                team_dict[club_name] = {}
                team_dict[club_name]['matches'] = int(cells[2].text)
                team_dict[club_name]['points'] = int(cells[3].text)
                team_dict[club_name]['win'] = int(cells[4].text)
                team_dict[club_name]['draw'] = int(cells[5].text)
                team_dict[club_name]['loose'] = int(cells[6].text)
                team_dict[club_name]['goals_shot'] = int(cells[7].text[:3])
                team_dict[club_name]['goals_lost'] = int(cells[7].text[-3:])

        return team_dict

    def create_team_objects(self, team_dict):
        Team.objects.all().delete()
        created_teams = None
        for team in team_dict:
            created_teams = Team.objects.create(
                name=team, matches=team_dict[team]['matches'],
                points=team_dict[team]['points'],
                win=team_dict[team]['win'], draw=team_dict[team]['draw'],
                loose=team_dict[team]['loose'],
                goals_shot=team_dict[team]['goals_shot'],
                goals_lost=team_dict[team]['goals_lost']
            )

        return created_teams

    def update_team_objects(self, team_dict):
        print('Uruchomiono update_team_objects()')
        updated_teams = None
        for team in Team.objects.all():
            if team.matches < team_dict[team.name]['matches']:
                updated_teams = Team.objects.filter(name=team).update(
                    matches=team_dict[team.name]['matches'],
                    points=team_dict[team.name]['points'],
                    win=team_dict[team.name]['win'],
                    draw=team_dict[team.name]['draw'],
                    loose=team_dict[team.name]['loose'],
                    goals_shot=team_dict[team.name]['goals_shot'],
                    goals_lost=team_dict[team.name]['goals_lost']
                )

        return updated_teams

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['created_teams'] = Team.objects.all()
        return context


class DownloadMatches(TemplateView):
    template_name = 'core/admin_matches.html'

    def download_matches(self):
        schedule = take_soup('http://www.pomorskifutbol.pl/liga.php?id=1309').find('table', class_='terminarz')
        matchweeks = schedule.find_all('tr')

        matches_dict = {}
        for data in matchweeks:
            matchweek = data.find_all('td', class_='kolejka')
            if matchweek:
                matchweek_number = int(matchweek[0].text[11:13])
                matches_dict[matchweek_number] = []

            home_team = data.find('td', class_='druzyna-1')
            away_team = data.find('td', class_='druzyna-2')
            goals = data.find('td', class_='wynik')
            date = data.find('td', class_='data-meczu')

            if home_team:
                match_dict = {}
                match_dict['matchweek_number'] = matchweek_number
                match_dict['home_team'] = home_team.text
                match_dict['away_team'] = away_team.text
                match_dict['home_team_goals'] = goals.text[1:3]
                match_dict['away_team_goals'] = goals.text[-2:]
                if date.text != '':
                    day = date.text.split(' ')[0].strip()
                    month = date.text.split(' ')[3][-2:]
                    year = date.text.split(' ')[3][:4]
                    try:
                        time = date.text.split(' ')[5]
                    except:
                        time = '00:00'
                    full_date = f"{day} {month} {year} {time}"
                    date_as_datetime = datetime.strptime(full_date, '%d %m %Y %H:%M')
                    match_dict['date'] = date_as_datetime
                elif date.text == '':
                    match_dict['date'] = "2021-01-01"

                matches_dict[matchweek_number].append(match_dict)

        return matches_dict

    def create_match_objects(self, matches_dict):

        MatchTest.objects.all().delete()
        created_matches = None
        for matchweek, list_of_dicts in matches_dict.items():
            for match in list_of_dicts:
                created_matches = MatchTest.objects.create(
                    match_week=match['matchweek_number'],
                    home_team=match['home_team'],
                    away_team=match['away_team'],
                    date=match['date'],
                    home_team_goals=match['home_team_goals'],
                    away_team_goals=match['away_team_goals']
                )

        return created_matches

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # context['created_matches'] = self.create_match_objects(self.download_matches())
        context['created_matches'] = MatchTest.objects.all()
        return context


class DownloadPlayers(TemplateView):
    template_name = 'core/admin_players.html'

    def download_players(self):
        url = 'https://regiowyniki.pl/druzyna/Pilka_Nozna/Pomorskie/Piast_Czluchow/kadra/'
        players_table = take_soup(url).find('table')
        players = players_table.find_all('tr')

        players_dict = {}
        for player in players:
            player_name = player.find('td')
            player_birthday = player.find('td', class_='text-muted')
            if player_name:
                players_dict[player_name.text] = {'first_name': (player_name.text).split(' ')[1],
                                                  'last_name': (player_name.text).split(' ')[0]}
            if player_birthday:
                players_dict[player_name.text]['birth_date'] = player_birthday.text

        return players_dict

    def create_players_objects(self, players_dict):
        created_players = None
        for player in players_dict:
            if not Player.objects.filter(
                    first_name=players_dict[player]['first_name'],
                    last_name=players_dict[player]['last_name']
            ):
                created_players = Player.objects.create(
                    first_name=players_dict[player]['first_name'],
                    last_name=players_dict[player]['last_name'],
                    birth_date=players_dict[player]['birth_date']
                )

        return created_players
