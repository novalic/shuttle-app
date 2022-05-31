from rest_framework import serializers

from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos.error import GEOSException
from rest_framework.exceptions import ValidationError

from ..models import ServiceArea


class AreaValidationSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(required=True)

    class Meta:
        model = ServiceArea
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise ValidationError('Field name is required.')

        return value

    def validate_provider(self, value):
        try:
            _ = int(value.id)
        except ValueError:
            raise ValidationError('Field provider has an incorrect type.')

        return value.id

    def validate_polygon(self, value):
        try:
            _ = Polygon(value)
        except GEOSException:
            raise ValidationError('Invalid polygon.')

        return value


class AreaUpdateValidationSerializer(AreaValidationSerializer):
    price = serializers.FloatField(required=True)

    class Meta:
        model = ServiceArea
        fields = '__all__'

    def validate_provider(self, value):
        try:
            _ = int(value.id)
        except ValueError:
            raise ValidationError('Field provider has an incorrect type.')

        obj_provider_id = self.context.get('area_provider_id')
        if value.id != obj_provider_id:
            raise ValidationError('Provider does not match.')

        return value.id


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ServiceAreaSerializer, self).to_representation(instance)
        data['polygon'] = instance.polygon.coords[0]
        return data

