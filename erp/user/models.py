from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords

from erp.base_model import BaseModel
from erp.user.managers import UserManager


class User(AbstractUser, BaseModel):
    USERNAME_FIELD = 'email'

    company = None

    username = None
    email = models.EmailField(_('Email address'), unique=True)

    REQUIRED_FIELDS = []

    objects = UserManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def short_name(self):
        return self.first_name
