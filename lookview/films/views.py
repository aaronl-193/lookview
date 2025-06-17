from datetime import datetime

from django import http
from django.shortcuts import render, HttpResponse
from django.utils import timezone

from .models import Film, FilmTag
from reviews.models import Review
from watchlist.models import Watchlist, WatchlistFilm

def film_view(request: http.HttpRequest, film_id: str, *args, **kwargs) -> HttpResponse:
    film_obj = Film.objects.get(id=film_id)
    context: dict = {
        'film': film_obj
    }
    return render(request, 'film.html', context)

def film_detail_view(
    request: http.HttpRequest,
    film_id: str,
) -> HttpResponse:
    film_obj: Film = Film.objects.get(id=film_id)
    film_ratings: (float, int) = Film.objects.find_film_rating_aggregate(film_obj.name)
    film_tags: list[FilmTag] = FilmTag.objects.find_tags_by_film(film_obj.id)
    film_reviews: list[Review] = Film.objects.find_film_reviews(film_obj.name)
    already_reviewed_films: models.QuerySet = [x.film for x in Review.objects.all().filter(site_user=request.user.site_user)]
    already_wishlisted_films: list[Film] = [x.film for x in WatchlistFilm.objects.filter(watchlist=request.user.site_user.watchlist)]
    
    already_reviewed: bool
    if film_obj in already_reviewed_films:
        already_reviewed = True
    else:
        already_reviewed = False

    already_wishlisted: bool
    if film_obj in already_wishlisted_films:
        already_wishlisted = True
    else:
        already_wishlisted = False

    context: dict = {
        'film': film_obj,
        'rating': film_ratings[0],
        'num_ratings': film_ratings[1],
        'tags': film_tags,
        'reviews': zip(
            film_reviews,
            [
                delta.days for delta in [
                    timezone.now() - review.date for review in film_reviews
                ]
            ]
        ),
        'reviewed': already_reviewed,
        'wishlisted': already_wishlisted,
    }
    return render(request, 'detail.html', context)

def catalog_view(
    request: http.HttpRequest,
) -> HttpResponse:
    query: str = request.GET.get('film')
    films_obj: models.QuerySet = [];
    if query != '' and query is not None:
        films_obj = Film.objects.find_film_by_name(query);
    else:
        films_obj = Film.objects.all();
    film_ratings: list[(float, int)] = [Film.objects.find_film_rating_aggregate(x.name) for x in films_obj]
    film_tags: list[FilmTag] = [FilmTag.objects.find_tags_by_film(x.id) for x in films_obj]
    
    already_reviewed_films: models.QuerySet = [x.film for x in Review.objects.all().filter(site_user=request.user.site_user)]
    already_wishlisted_films: list[Film] = [x.film for x in WatchlistFilm.objects.filter(watchlist=request.user.site_user.watchlist)]
    
    new_films_reviewed = []
    for film in films_obj:
        if film in already_reviewed_films:
            new_films_reviewed.append(True)
        else:
            new_films_reviewed.append(False)
    
    new_films_watchlisted = []
    for film in films_obj:
        if film in already_wishlisted_films:
            new_films_watchlisted.append(True)
        else:
            new_films_watchlisted.append(False)
    
    films = zip(
        film_ratings,
        film_tags,
        films_obj,
        new_films_reviewed,
        new_films_watchlisted,
    )
    context: dict = {
        'films': films,
    }
    return render(request, 'catalog.html', context)
