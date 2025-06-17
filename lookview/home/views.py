from datetime import datetime

from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse

from films.models import FilmTag, Film
from algorithm.models import Algorithm
from reviews.models import Review
from watchlist.models import WatchlistFilm

def homepage_view(request: http.HttpRequest, *args, **kwargs) -> HttpResponse:
    if request.user.is_authenticated:
        favorite_tags: dict[FilmTag, int] = Algorithm.objects.get_algorithm(
            request.user.site_user.algorithm.id
        )
        three: list[FilmTag] = []
        count = 0
        for tag in sorted(favorite_tags.items(), key=lambda x: x[1]):
            if count == 3:
                break
            three.append(tag[0])
            count += 1
        top_unwatched_films: models.QuerySet = Film.objects.all().filter(
            tags__in=three
        ).exclude(
            watchlist_films__watchlist__site_user=request.user.site_user
        ).exclude(
            reviews__site_user=request.user.site_user
        )
        for film in top_unwatched_films:
            film.aggregate = Film.objects.find_film_rating_aggregate(film.name)[0]
        print(top_unwatched_films)
        final_films = top_unwatched_films.order_by('aggregate').distinct()[:4]
        final_films_ratings: list[(float, int)] = [Film.objects.find_film_rating_aggregate(film.name) for film in final_films]
        final_films_tags: list[models.QuerySet] = [
            FilmTag.objects.find_tags_by_film(film_id=film.id) for film in final_films
        ]
        today = datetime.today()
        new_films = Film.objects.all().filter(
            release_date__year=today.year
        ).filter(
            release_date__month=today.month
        )
        new_films_ratings: list[(float, int)] = [Film.objects.find_film_rating_aggregate(film.name) for film in new_films]
        new_films_tags: list[models.QuerySet] = [
            FilmTag.objects.find_tags_by_film(film_id=film.id) for film in new_films
        ]
        already_reviewed_films: models.QuerySet = [x.film for x in Review.objects.all().filter(site_user=request.user.site_user)]
        already_wishlisted_films: list[Film] = [x.film for x in WatchlistFilm.objects.filter(watchlist=request.user.site_user.watchlist)]
        
        print(already_wishlisted_films)

        new_films_reviewed = []
        for film in new_films:
            if film in already_reviewed_films:
                new_films_reviewed.append(True)
            else:
                new_films_reviewed.append(False)
        
        new_films_watchlisted = []
        for film in new_films:
            if film in already_wishlisted_films:
                new_films_watchlisted.append(True)
            else:
                new_films_watchlisted.append(False)

        main_film: Film = (lambda x: next(iter(final_films)) if len(x) > 0  else {"id": 0, "name": "Tidak Ada :(", "description": "Tidak ada rekomendasi film baru, mulai review film untuk menerima rekomendasi."})(final_films)

        context: dict = {
            'film_recommendations': zip(final_films_ratings, final_films, final_films_tags),
            'main_recommendation': main_film,
            'new_films': zip(new_films_ratings, new_films, new_films_tags, new_films_reviewed, new_films_watchlisted),
        }
        return render(request, 'index.html', context)
    return redirect('login')