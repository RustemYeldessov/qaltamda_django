from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Section(SafeDeleteModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta(SafeDeleteModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_section')
        ]
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.name
