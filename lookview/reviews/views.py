from datetime import datetime

from django import http
from django.shortcuts import render, redirect, HttpResponse

from films.models import Film, FilmTag
from reviews.models import Review
from users.models import SiteUser

def review_film_view(
    request: http.HttpRequest,
    film_id: str,
) -> HttpResponse:
    film_obj: Film = Film.objects.get(id=film_id)
    if request.method == "GET":
        film_ratings: (float, int) = Film.objects.find_film_rating_aggregate(film_obj.name)
        film_tags: list[FilmTag] = FilmTag.objects.find_tags_by_film(film_obj.id)
        context: dict = {
            'film': film_obj,
            'rating': film_ratings[0],
            'num_ratings': film_ratings[1],
            'tags': film_tags,
        }
        return render(request, 'review.html', context)
    elif request.method == "POST":
        rating: int = request.POST.get("rating")
        rating_text: str = request.POST.get("review-text")
        site_user: SiteUser = SiteUser.objects.get(user=request.user)
        review: Review = Review.objects.create_review(
            site_user,
            film_obj,
            rating,
            rating_text,
        )
        return redirect('users', request.user.username)

