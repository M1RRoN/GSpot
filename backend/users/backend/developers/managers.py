from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce


class CompanyQuerySet(models.QuerySet):
    def with_workers_count(self):
        return self.annotate(
            workers_count=Coalesce(Count('username'), 0)
        )


class CompanyManager(models.Manager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db)

    def get_workers_count(self):
        return self.get_queryset().with_workers_count()
