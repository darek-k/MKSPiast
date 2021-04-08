from django.contrib import admin

from core.models import Article, Comment, Team, Match, MatchWeek, Player, NextMatchWeek, MatchTest


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_date'
    fields = ('title', 'text', 'author', 'image')


admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(MatchWeek)
admin.site.register(Player)
admin.site.register(NextMatchWeek)

admin.site.register(MatchTest)
