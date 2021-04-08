from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='articles', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.author} ({self.published_date})'

    class Meta:
        ordering = ['-published_date', ]


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='comments')
    author = models.CharField(max_length=20)
    text = models.TextField(max_length=1000)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.text}'

    class Meta:
        ordering = ['-published_date', ]


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    matches = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    loose = models.IntegerField(default=0)
    goals_shot = models.IntegerField(default=0)
    goals_lost = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-points', '-goals_shot', '-goals_lost', 'name']


class MatchWeek(models.Model):  # todo: czy potrzebne?
    week = models.IntegerField(null=True, unique=True)

    # match = models.ForeignKey(Match, on_delete=models.DO_NOTHING, related_name='matches', default='')

    def __str__(self):
        return f'{self.week}. kolejka'

    class Meta:
        ordering = ['-week']
        verbose_name_plural = 'Match Weeks'


class NextMatchWeek(models.Model):  # todo: czy potrzebne?
    match_week = models.ForeignKey(MatchWeek, on_delete=models.CASCADE, related_name='next_match_weeks', null=True)

    def __str__(self):
        return f'{self.match_week}'

    class Meta:
        verbose_name_plural = 'Next matchweek'


class Match(models.Model):
    match_week = models.ForeignKey(MatchWeek, on_delete=models.CASCADE, related_name='match_weeks', null=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')
    date = models.DateTimeField()
    home_team_goals = models.IntegerField(null=True, blank=True)
    away_team_goals = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.match_week} - {self.home_team} vs {self.away_team} / {self.date}'

    class Meta:
        ordering = ['match_week', 'date']
        verbose_name_plural = 'Matches'


# todo: tworzy obiekty potrzebne tylko do tabeli; można to zmienić żeby obiekty
# todo: były powiązane z innymi za pomocą ForeignKey - ale wtedy użyj modelu Match
class MatchTest(models.Model):
    match_week = models.IntegerField()
    home_team = models.CharField(max_length=20)
    away_team = models.CharField(max_length=20)
    date = models.DateTimeField(null=True)
    home_team_goals = models.CharField(max_length=20, default='-')
    away_team_goals = models.CharField(max_length=20, default='-')

    def __str__(self):
        return f'{self.home_team} {self.home_team_goals}-{self.away_team_goals} {self.away_team}'

    class Meta:
        ordering = ['-match_week', 'date']


class Player(models.Model):
    GOALKEEPER = 'Bramkarz'
    DEFENDER = 'Obrońca'
    MIDFIELDER = 'Pomocnik'
    FORWARD = 'Napastnik'
    POSITION_CHOICES = [
        (GOALKEEPER, 'Bramkarz'), (DEFENDER, 'Obrońca'), (MIDFIELDER, 'Pomocnik'), (FORWARD, 'Napastnik'),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True)
    number = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='players', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        ordering = ['position', 'last_name', 'first_name']
        unique_together = ['first_name', 'last_name']
