import pycountry

from rest_framework import serializers

from rest_framework.exceptions import ValidationError

from ..models import Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'
        read_only_fields = ('id', 'timestamp')

    def validate_language(self, value):
        try:
            _ = pycountry.languages.lookup(value)
        except LookupError:
            raise ValidationError(f'Invalid value for language: {value}.')

        return value

    def validate_currency(self, value):
        try:
            _ = pycountry.currencies.lookup(value)
        except LookupError:
            raise ValidationError(f'Invalid value for currency: {value}.')

        return value
