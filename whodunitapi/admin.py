from django.contrib import admin

from whodunitapi.models import  Genre, Movie, Player, MovieNight, Suspect, Guilty, MovieSuspect

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Player)
admin.site.register(MovieNight)
admin.site.register(Suspect)
admin.site.register(Guilty)
admin.site.register(MovieSuspect)