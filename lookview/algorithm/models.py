from django.db import models as db_models
from reviews import models as rv_models
from films import models as fm_models

class AlgorithmManager(db_models.Manager):
    def create_algorithm(
        self,
        site_user: 'users.SiteUser',
    ):
        algorithm: Algorithm = self.create(
            site_user = site_user
        )
        return algorithm
    
    def process_data(self, algorithm_id: int) -> dict[fm_models.FilmTag, int]:
        algorithm: 'Algorithm' = self.get(id=algorithm_id)
        review_query: db_models.QuerySet = rv_models.Review.objects.find_review_by_user(
            algorithm.site_user.user.username
        )
        tags: dict[str, int] = {};
        weight_table: list = [-5, -3, 1, 4, 7]
        for review in review_query:
            tags_query: db_models.QuerySet = fm_models.FilmTag.objects.find_tags_by_film(review.film.id)
            for tag in tags_query:
                if tag.name not in tags:
                    tags[tag] = weight_table[review.rating - 1]
                else:
                    tags[tag] += weight_table[review.rating - 1]
        return tags
    
    def get_algorithm(self, algorithm_id: int) -> dict[fm_models.FilmTag, int]:
        return self.process_data(algorithm_id)

class Algorithm(db_models.Model):
    site_user: db_models.OneToOneField = db_models.OneToOneField(
        'users.SiteUser',
        on_delete = db_models.CASCADE,
        related_name="algorithm",
    )
    algorithm_dict: dict[fm_models.FilmTag, int] = {}
    objects: AlgorithmManager = AlgorithmManager()