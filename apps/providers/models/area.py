from django.contrib.gis.db import models

from .provider import Provider


class ServiceArea(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )
    price = models.FloatField(
        default=0.0
    )

    polygon = models.PolygonField()

    provider = models.ForeignKey(
        Provider,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False
    )
