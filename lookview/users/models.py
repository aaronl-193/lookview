import datetime

from django.conf import settings
from django.db import models as db_models
from django.contrib.auth import models as auth_models

from watchlist import models as wl_models
from algorithm import models as al_models

class SiteUserManager(db_models.Manager):
    def create_site_user(
        self,
        user: auth_models.User,
        date_of_birth: datetime.date = None,
    ) -> 'SiteUser':
        site_user: SiteUser = self.create(
            user = user,
            date_of_birth = date_of_birth,
            description = "",
        )
        wl_models.Watchlist.objects.create_watchlist(site_user)
        al_models.Algorithm.objects.create_algorithm(site_user)
        return site_user

class SiteUser(db_models.Model):
    user: db_models.OneToOneField = db_models.OneToOneField(
        auth_models.User,
        on_delete = db_models.CASCADE,
        related_name = "site_user",
    )
    date_of_birth: db_models.DateField = db_models.DateField(
        default = None,
        blank = True,
        null = True,
    )
    description: db_models.TextField = db_models.TextField(
        max_length = 1000,
        null = True,
        blank = True,
    )
    profile_picture: db_models.ImageField = db_models.ImageField(
        default = "default-pfp.png",
    )
    objects: SiteUserManager = SiteUserManager()
