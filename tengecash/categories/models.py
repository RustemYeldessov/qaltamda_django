from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class Category(SafeDeleteModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta(SafeDeleteModel.Meta):
        # Это гарантирует, что у одного пользователя не будет двух одинаковых названий
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_category')
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
