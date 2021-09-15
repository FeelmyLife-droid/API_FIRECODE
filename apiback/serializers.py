from rest_framework import serializers
from apiback.models import City, Street, Shop


class CityListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']

    def validate_title(self, value):
        return value.title()


class StreetInCitySerializers(serializers.ModelSerializer):
    city_title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Street
        fields = ['id', 'title', 'city_title']


class StreetCreatInCitySerializers(serializers.ModelSerializer):
    city_title = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Street
        fields = ['id', 'title', 'city_title']

    def validate_title(self, value):
        return value.title()


class ShopListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'title', 'city', 'street', 'house', 'time_open', 'time_close']

    def validate_title(self, value):
        return value.title()


class ShopListSerializers(serializers.ModelSerializer):
    city = serializers.StringRelatedField(source='city.title')
    street = serializers.StringRelatedField(source='street.title')

    class Meta:
        model = Shop
        fields = ['id', 'title', 'city', 'street', 'house', 'time_open', 'time_close']

    def validate_title(self, value):
        return value.title()
