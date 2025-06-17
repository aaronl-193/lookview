from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class ReviewManager(models.Manager):
    def create_review(
        self,
        site_user: 'users.SiteUser',
        film: 'films.Film',
        rating: int,
        text: str,
    ) -> 'Review':
        review: Review = self.create(
            site_user = site_user,
            film = film,
            title = "",
            description = text,
            rating = rating,
            date = datetime.now(),
            liked = 0,
        )
        return review
    
    def find_review_by_user(self, username: str) -> models.QuerySet:
        return self.filter(site_user__user__username=username)
    
    def find_review_by_film(self, film_name: str) -> models.QuerySet:
        return self.filter(film__name=film_name)
    
    def find_review(self, review_id: int) -> 'Review':
        return self.get(id=review_id)
    
    def increment_review_liked(self, review_id: int) -> None:
        self.get(id=review_id).liked += 1

class Review(models.Model):
    site_user: models.ForeignKey = models.ForeignKey(
        'users.SiteUser',
        on_delete = models.CASCADE,
    )
    film: models.ForeignKey = models.ForeignKey(
        'films.Film',
        on_delete = models.CASCADE,
        related_name = "reviews",
    )
    title: models.TextField = models.TextField(null=True)
    description: models.TextField = models.TextField(null=True)
    rating: models.PositiveIntegerField = models.PositiveIntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    liked: models.PositiveIntegerField = models.PositiveIntegerField()
    date: models.DateField = models.DateTimeField()
    objects: ReviewManager = ReviewManager()

    class Meta:
        unique_together = ('site_user', 'film')
