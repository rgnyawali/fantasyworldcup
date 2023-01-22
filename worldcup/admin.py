from django.contrib import admin
from worldcup.models import Team, Match, KnockOutTeamSelection, Score, LeaderBoard, Comment

# Register your models here.
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(KnockOutTeamSelection)
admin.site.register(Score)
admin.site.register(LeaderBoard)
admin.site.register(Comment)
