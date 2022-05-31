from django.contrib.gis.geos import Polygon
from django.db import migrations


def populate_world_areas(apps, schema_editor):
    WorldArea = apps.get_model('parameters', 'WorldArea')

    world_areas = list()

    for latitude in range(-90, 90):
        for longitude in range(-180, 180):
            world_areas.append(
                WorldArea(
                    square=Polygon([
                        [latitude, longitude],
                        [latitude, longitude + 1],
                        [latitude + 1, longitude + 1],
                        [latitude + 1, longitude],
                        [latitude, longitude]
                    ]),
                    code=f'{latitude}_{longitude}')
            )
    _ = WorldArea.objects.bulk_create(world_areas)


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_world_areas)
    ]
