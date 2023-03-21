from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce


class CompanyUserManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .annotate(workers_count=Coalesce(Count('username'), 0))
        )
