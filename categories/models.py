from typing import List

from django.db import models
from django.contrib.contenttypes.models import ContentType


class Category(models.Model):
    parent = models.ForeignKey(
        to="self",
        blank=True,
        null=True,
        related_name="children",
        verbose_name="Parent",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Name of category", max_length=256, unique=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}({self.pk})"

    @property
    def parents(self) -> List:
        result = []
        parent = self.parent
        while parent:
            result.append(parent)
            parent = parent.parent
        return result

    @property
    def children(self) -> models.QuerySet:
        return self.children.all()

    @property
    def siblings(self) -> models.QuerySet:
        content_type = ContentType.objects.get_for_model(self)
        model = content_type.model_class()
        return model.objects.filter(parent=self.parent).exclude(pk=self.pk)
