from datetime import datetime

from django.db import models

from films.models import Film
from reviews.models import Review
from users.models import SiteUser

class SiteUserCommentManager(models.Manager):
    def create_comment(
        self,
        author: SiteUser,
        target: Film,
        content: str,
    ) -> 'Review':
        comment: SiteUserComment = self.create(
            author = author,
            target = target,
            content = content,
            comment_created = datetime.now()
        )
        return comment

class SiteUserComment(models.Model):
    author: models.ForeignKey = models.ForeignKey(
        SiteUser,
        on_delete = models.CASCADE,
        null = False,
        related_name = "comments",
    )
    target: models.ForeignKey = models.ForeignKey(
        Film,
        on_delete = models.CASCADE,
        null = False,
        related_name = "comments",
    )
    content: models.TextField = models.TextField(
        max_length = 512,
        blank = False,
    )
    comment_created = models.TimeField()
    objects: SiteUserCommentManager = SiteUserCommentManager()
