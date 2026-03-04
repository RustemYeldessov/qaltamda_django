from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from safedelete.managers import SafeDeleteManager

class CustomUserManager(SafeDeleteManager, UserManager):
    pass

class User(AbstractUser, SafeDeleteModel):
    first_name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name=_("Last Name")
    )
    USERNAME_FIELD = 'username'
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    _safedelete_policy = SOFT_DELETE_CASCADE
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
