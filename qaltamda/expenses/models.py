from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from qaltamda.categories.models import Category
from qaltamda.sections.models import Section

User = get_user_model()

class Expense(SafeDeleteModel):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Section")
    )
    date = models.DateField(
        default=timezone.now,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Category")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("1"))],
        verbose_name=_("Amount")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses_created",
        verbose_name=_("Author")
    )
    _safedelete_policy = SOFT_DELETE_CASCADE

    def __str__(self):
        return f"{self.description} - {self.amount}"

    class Meta(SafeDeleteModel.Meta):
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
