from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Shop(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, verbose_name="id"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.CASCADE
    )
    priority = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="priority",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.CharField(
        max_length=224, blank=False, null=False, verbose_name="title"
    )
    due_date = models.DateTimeField(verbose_name="due date", blank=False, null=False)
    is_complete = models.BooleanField(default=False, verbose_name="is complete")
    description = models.TextField(verbose_name="description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    quantity = models.IntegerField(blank=False, null=False, default=0)
