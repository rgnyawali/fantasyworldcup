from django.contrib import admin
from .models import Player, Game, CurrentPlayer

# Register your models here.
admin.site.register(Player)
admin.site.register(CurrentPlayer)
admin.site.register(Game)

