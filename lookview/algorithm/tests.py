import datetime

from django.test import TestCase
from django.contrib.auth import models as auth_models

from algorithm import models as al_models
from users import models as us_models
from films import models as fm_models
from reviews import models as rv_models

class AlgorithmTestCase(TestCase):
    def test_one(self):
        user: auth_models.User = auth_models.User.objects.create_user(
            username="test",
            password="test",
        )
        site_user: us_models.SiteUser = us_models.SiteUser.objects.create_site_user(user)

        film_1: fm_models.Film = fm_models.Film.objects.create_film("Test1", "Test1", "Test1")
        film_2: fm_models.Film = fm_models.Film.objects.create_film("Test2", "Test2", "Test2")
        film_3: fm_models.Film = fm_models.Film.objects.create_film("Test3", "Test3", "Test3")

        film_tag_1: fm_models.FilmTag = fm_models.FilmTag.objects.create_film_tag("TestTag1")
        film_tag_2: fm_models.FilmTag = fm_models.FilmTag.objects.create_film_tag("TestTag2")
        film_tag_3: fm_models.FilmTag = fm_models.FilmTag.objects.create_film_tag("TestTag3")

        film_tag_1.films.add(film_1)
        film_tag_2.films.add(film_1)
        film_tag_2.films.add(film_2)
        film_tag_3.films.add(film_1)
        film_tag_1.films.add(film_3)

        review_1: rv_models = rv_models.Review.objects.create_review(site_user, film_1, 5)
        review_2: rv_models = rv_models.Review.objects.create_review(site_user, film_2, 1)
        review_3: rv_models = rv_models.Review.objects.create_review(site_user, film_3, 3)

        print(fm_models.Film.objects.find_film_rating_aggregate(film_1.name))

        algorithm: al_models.Algorithm = al_models.Algorithm.objects.get(site_user=site_user)
        al_models.Algorithm.objects.process_data(algorithm.id)
