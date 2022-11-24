from django.contrib import admin

from .models import Team, Match, TeamScore 

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(TeamScore)