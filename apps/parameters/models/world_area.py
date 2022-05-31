from django.contrib.gis.db import models


class WorldArea(models.Model):
    code = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        unique=True
    )
    square = models.PolygonField()
