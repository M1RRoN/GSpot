from django.db import models
from django.db.models import Count


class CompanyManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(workers_count=Count('companyemployee'))
        return queryset


class CompanyEmployeeQuerySet(models.QuerySet):
    def available_workers_for_company(self, company_id):
        return self.filter(company_id=company_id).select_related('company')


class CompanyEmployeeManager(models.Manager):
    def get_queryset(self):
        return CompanyEmployeeQuerySet(self.model, using=self._db)

    def available_workers_for_company(self, company_id):
        return self.get_queryset().available_workers_for_company(company_id)
