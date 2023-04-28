from django.contrib import admin
from movie_app.models import Movie,MovieCollection


admin.site.register(MovieCollection)


class MovieAdmin(admin.ModelAdmin):
    list_display = ["title","genere"]
admin.site.register(Movie,MovieAdmin)
