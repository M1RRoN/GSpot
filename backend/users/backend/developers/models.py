import uuid

from django.db import models

from common.models import BaseUser, Country
from developers.managers import CompanyManager


class CompanyUser(BaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    avatar = models.ImageField(blank=True, upload_to='backend/users/backend/static/img/%Y/%m/%d')
    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)

    objects = CompanyManager()


class DeveloperFriends(models.Model):
    id = models.IntegerField(primary_key=True)
    user1 = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='user2_friends')


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.OneToOneField(CompanyUser, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    image = models.ImageField(blank=True, upload_to='backend/users/backend/static/img/%Y/%m/%d')
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class CompanyEmployee(models.Model):
    user_id = models.OneToOneField(CompanyUser, on_delete=models.PROTECT, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class ContactType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    icon = models.ImageField(blank=True, upload_to='backend/users/backend/static/icon')


class Contacts(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(ContactType, on_delete=models.PROTECT)
    value = models.CharField(max_length=50)


class CompanyContact(models.Model):
    id = models.IntegerField(primary_key=True)
    contact = models.ForeignKey(Contacts, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class ContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=50)
    app_label = models.CharField(max_length=50)
    model = models.CharField(max_length=50)


class DeveloperPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50)


class DeveloperUserPermissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission = models.ForeignKey(PermissionDeveloper, on_delete=models.PROTECT)
    user = models.ForeignKey(CompanyUser, on_delete=models.PROTECT)


class DeveloperGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)


class DeveloperGroupPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    permission = models.ForeignKey(DeveloperPermission, on_delete=models.PROTECT)
    group = models.ForeignKey(DeveloperGroup, on_delete=models.PROTECT)


class DeveloperGroupUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(DeveloperGroup, on_delete=models.PROTECT)
    user = models.ForeignKey(CompanyUser, on_delete=models.PROTECT)
