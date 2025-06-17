from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser

from .models import SiteUser
from watchlist.models import WatchlistFilm
from reviews.models import Review
from films.models import FilmTag, Film
from algorithm.models import Algorithm

def user_page_view(
    request: http.HttpRequest,
    username: str,
) -> HttpResponse:
    site_user_obj: SiteUser = SiteUser.objects.get(user__username=username)
    film_tag_dict: dict[FilmTag, int] = Algorithm.objects.get_algorithm(
        site_user_obj.algorithm.id,
    )
    film_tag_mode: FilmTag = max(film_tag_dict, key=film_tag_dict.get)
    reviews: models.QuerySet = Review.objects.find_review_by_user(site_user_obj.user.username)
    watchlist: models.QuerySet = WatchlistFilm.objects.find_films_per_watchlist(site_user_obj)
    watchlist_tags: list[models.QuerySet] = [
        FilmTag.objects.find_tags_by_film(film_id=wfilm.film.id) for wfilm in watchlist
    ]
    film_ratings: list[(float, int)] = [
        Film.objects.find_film_rating_aggregate(wfilm.film.name) for wfilm in watchlist
    ]
    context: dict = {
        'user': site_user_obj.user,
        'siteuser': site_user_obj,
        'lenlist': len(watchlist),
        'watchlist': zip(watchlist_tags, watchlist, film_ratings),
        'lenreview': len(reviews),
        'reviews': reviews,
        'mode_tag': film_tag_mode.name,
    }
    # user_obj = User.objects.get(username=query_username)
    page: str = ""
    if request.user.username == site_user_obj.user.username:
        page = "profile.html"
    else:
        page = "profile-other.html"
    return render(request, page, context)

def forum_view(
    request: http.HttpRequest,
) -> HttpResponse:
    return render(request, "discussion.html", {})

def user_outside_view(
    request: http.HttpRequest,
    username: str,
) -> HttpResponse:
    if (request.user.username != username):
        return redirect("users", username)
    site_user_obj: SiteUser = SiteUser.objects.get(user__username=username)
    film_tag_dict: dict[FilmTag, int] = Algorithm.objects.get_algorithm(
        site_user_obj.algorithm.id,
    )
    try:
        film_tag_mode: FilmTag = max(film_tag_dict, key=film_tag_dict.get)
        reviews: models.QuerySet = Review.objects.find_review_by_user(site_user_obj.user.username)
        watchlist: models.QuerySet = WatchlistFilm.objects.find_films_per_watchlist(site_user_obj)
        print(len(reviews))
        watchlist_tags: list[models.QuerySet] = [
            FilmTag.objects.find_tags_by_film(film_id=wfilm.film.id) for wfilm in watchlist
        ]
        film_ratings: list[(float, int)] = [
            Film.objects.find_film_rating_aggregate(wfilm.film.name) for wfilm in watchlist
        ]
        context: dict = {
            'user': site_user_obj.user,
            'siteuser': site_user_obj,
            'lenlist': len(watchlist),
            'watchlist': zip(watchlist_tags, watchlist, film_ratings),
            'lenreview': len(reviews),
            'reviews': reviews,
            'mode_tag': film_tag_mode.name,
        }
    except ValueError:
        context: dict = {
            'user': site_user_obj.user,
            'siteuser': site_user_obj,
            'lenlist': 0,
            'watchlist': None,
            'lenreview': 0,
            'reviews': None,
            'mode_tag': None,
        }
    page = "profile-other.html"
    return render(request, page, context)