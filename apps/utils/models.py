from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True, on_delete=CASCADE)
    credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
    pass