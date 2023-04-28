import uuid

from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    GENRES = (
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Science Fiction', 'Science Fiction'),
        ('Action', 'Action'),
        ('Romance', 'Romance'),
        ('Comedy', 'Comedy')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    genere = models.CharField(max_length=32, choices=GENRES)

    def __str__(self):
        return self.title


class MovieCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
