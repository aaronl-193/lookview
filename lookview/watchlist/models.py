from django.db import models

from films.models import Film

class WatchlistManager(models.Manager):
    def create_watchlist(
        self,
        site_user: 'users.SiteUser',
    ) -> 'Watchlist':
        watchlist: Watchlist = self.create(
            site_user = site_user
        )
        return watchlist

class Watchlist(models.Model):
    site_user: models.OneToOneField = models.OneToOneField(
        'users.SiteUser',
        related_name = "watchlist",
        on_delete = models.CASCADE,
    )
    objects: WatchlistManager = WatchlistManager()

class WatchlistFilmManager(models.Manager):
    def create_watchlist_film(
        self,
        watchlist: Watchlist,
        film: Film,
    ) -> 'WatchlistFilm':
        watchlist_film: WatchlistFilm = self.create(
            watchlist = watchlist,
            film = film,
        )
        return watchlist_film
    
    def find_films_per_watchlist(
        self,
        site_user: 'users.SiteUser',
    ) -> models.QuerySet:
        return self.filter(watchlist=site_user.watchlist)

class WatchlistFilm(models.Model):
    watchlist: models.ForeignKey = models.ForeignKey(
        Watchlist,
        related_name = "watchlist_films",
        on_delete = models.CASCADE,
    )
    film: models.ForeignKey = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name="watchlist_films",
    )
    objects: models.Manager = WatchlistFilmManager()

    class Meta:
        unique_together = ('watchlist', 'film')
