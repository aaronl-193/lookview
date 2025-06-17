import statistics
from datetime import datetime

from django.db import models

from reviews.models import Review

class FilmManager(models.Manager):
    def create_film(
        self,
        name: str,
        duration: int,
        description: str,
        director: str,
        studio: str,
        actors: str,
        release_date: datetime,
    ) -> 'Film':
        film: Film = self.create(
            name = name,
            duration = duration,
            description = description,
            director = director,
            studio = studio,
            actors = actors,
            release_date = release_date,
        )
        return film

    def find_film_by_name(self, film_name: str) -> models.QuerySet:
        return self.filter(name__contains=film_name)
    
    def find_film_rating_aggregate(self, film_name: str) -> (float, int):
        reviews: models.QuerySet = Review.objects.find_review_by_film(film_name)
        if len(reviews) == 0:
            return (0.0, 0)
        average: float = statistics.mean([float(x.rating) for x in reviews])
        Film.objects.get(name=film_name).aggregate = average
        return (average, len(reviews))
    
    def find_film_reviews(self, film_name: str) -> list:
        return list(Review.objects.find_review_by_film(film_name))

class Film(models.Model):
    name: models.TextField = models.TextField(max_length=128, unique=True)
    duration: models.IntegerField = models.IntegerField()
    description: models.TextField = models.TextField(max_length=1024)
    director: models.TextField = models.TextField(max_length=128)
    studio: models.TextField = models.TextField(max_length=128)
    actors: models.TextField = models.TextField(max_length=256)
    release_date: models.DateField = models.DateField()
    poster: models.ImageField = models.ImageField(
        default="default.png",
        blank=False,
        null=False,
    )
    aggregate: float = models.IntegerField(default=0)
    objects: models.Manager = FilmManager()

class FilmTagManager(models.Manager):
    def create_film_tag(
        self,
        name: str,
    ) -> 'FilmTag':
        film_tag: FilmTag = self.create(
            name = name,
        )
        return film_tag
    
    def find_tags_by_film(self, film_id: str) -> models.QuerySet:
        return self.filter(films__id=film_id)

class FilmTag(models.Model):
    name: models.TextField = models.TextField(max_length=32)
    films: models.ManyToManyField = models.ManyToManyField(
        Film,
        blank=True,
        related_name="tags",
    )
    objects: FilmTagManager = FilmTagManager()
