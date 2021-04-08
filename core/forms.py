import re

from core.models import Comment, Article, Team, Match, MatchWeek, Player, NextMatchWeek
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        labels = {
            'author': '', 'text': '',
        }
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'text': forms.Textarea(attrs={'placeholder': 'Twój komentarz'}),
        }

    def clean_text(self):
        initial = self.cleaned_data['text']
        bad_words = ['kurwa', 'kurwy', 'kurwe', 'kurwę', 'kurwo', 'chuj', 'chuje', 'chuja', 'chujowy', 'chujowe',
                     'chujowa', 'jebać', 'jebac', 'jebany', 'jebana', 'jebane', ]
        words = re.sub(r'\s*\.\s*', ' ', initial).split(' ')
        print('WORDS: ', words)
        without_bad_words = ' '.join('*' * len(word) if word in bad_words else word for word in words)

        sentences = re.sub(r'\s*\.\s*', '.', without_bad_words).split('.')

        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)

        return cleaned


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'author', 'image')
        labels = {
            'title': 'Tytuł', 'text': 'Tekst', 'author': 'Autor', 'image': 'Zdjęcie',
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'matches', 'points', 'win', 'draw', 'loose', 'goals_shot', 'goals_lost', 'logo')
        labels = {
            'name': 'Nazwa', 'points': 'Punkty', 'win': 'Zwycięstwa', 'loose': 'Porażki', 'draw': 'Remisy',
            'goals_shot': 'Gole strzelone', 'goals_lost': 'Gole stracone', 'logo': 'Logo',
        }


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('match_week', 'home_team', 'away_team', 'date', 'home_team_goals', 'away_team_goals')
        labels = {
            'match_week': 'Kolejka', 'home_team': 'Gospodarze', 'away_team': 'Goście', 'date': 'Data',
            'home_team_goals': 'Gospodarze - liczba goli', 'away_team_goals': 'Goście - liczba goli',
        }
        widgets = {
            'date': forms.DateInput(format='%D/%M/%Y'),
            'time': forms.TimeInput(format='%H:%M'),
        }
        help_texts = {
            'date': ('Format: DD.MM.RRR'),
            'time': ('Format: GG:MM'),
        }


class MatchWeekForm(forms.ModelForm):
    class Meta:
        model = MatchWeek
        fields = ('week',)
        labels = {'week': 'Kolejka'}


class NextMatchWeekForm(forms.ModelForm):
    class Meta:
        model = NextMatchWeek
        fields = ('match_week',)
        labels = {'match_week': 'Następna kolejka'}
        help_text = {'match_week': 'Nie dodawaj nowych kolejek, zawsze edytuj istniejącą'}


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'birth_date', 'position')
        labels = {'first_name': 'Imię', 'last_name': 'Nazwisko', 'birth_date': 'Data urodzenia', 'position': 'Pozycja'}
