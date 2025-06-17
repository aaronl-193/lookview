from django import http
from django.shortcuts import render
from django.http import HttpResponse

import watchlist.models as wl_models
import users.models as us_models
import films.models as fm_models

def watchlist_view(
    request: http.HttpRequest,
    username: str,
) -> HttpResponse:
    if request.method == "POST":
        film_id: int = request.POST.get("film")
        film: fm_models = fm_models.Film.objects.get(id=film_id)
        site_user: us_models.SiteUser = us_models.SiteUser.objects.get(user=request.user)
        watchlist: wl_models.Watchlist = wl_models.Watchlist.objects.get(site_user=site_user)
        if film not in [x.film for x in wl_models.WatchlistFilm.objects.filter(watchlist__id=watchlist.id)]:
            wl_models.WatchlistFilm.objects.create_watchlist_film(watchlist, film)
        else:
            wl_models.WatchlistFilm.objects.get(watchlist=watchlist, film=film).delete()
    site_user_obj: us_models.SiteUser = us_models.SiteUser.objects.get(
        user__username = username
    )
    watchlist: models.QuerySet = wl_models.WatchlistFilm.objects.find_films_per_watchlist(site_user_obj)
    watchlist_tags: list[models.QuerySet] = [
        fm_models.FilmTag.objects.find_tags_by_film(film_id=wfilm.film.id) for wfilm in watchlist
    ]
    watchlist_ratings: list[(float, int)] = [
        fm_models.Film.objects.find_film_rating_aggregate(wfilm.film.name) for wfilm in watchlist
    ]
    context: dict = {
        'user': site_user_obj.user,
    }
    if request.user.username == site_user_obj.user.username:
        context['watchlist'] = zip(watchlist_tags, watchlist, watchlist_ratings)
    else:
        pass
    return render(request, 'watchlist.html', context)
