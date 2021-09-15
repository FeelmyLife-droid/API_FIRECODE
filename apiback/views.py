import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apiback.models import City, Street, Shop
from apiback.serializers import CityListCreateSerializers, StreetInCitySerializers, StreetCreatInCitySerializers, \
    ShopListCreateSerializers, ShopListSerializers


def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


class CityListCreate(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityListCreateSerializers

    @action(methods=['GET', 'POST'], detail=True)
    def street(self, request, pk):
        if not City.objects.filter(pk=pk).exists():
            return Response({"error": "This city id doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            query = Street.objects.select_related().filter(city_title__pk=pk)
            serializer = StreetInCitySerializers(query, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        elif request.method == 'POST':
            if not Street.objects.filter(city_title_id=pk, title=request.data['title'].title()).exists():
                request.data['city_title'] = pk
                serializer = StreetCreatInCitySerializers(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "This street id already exists."}, status=status.HTTP_400_BAD_REQUEST)


class ShopListCreate(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopListCreateSerializers

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShopListSerializers
        return ShopListCreateSerializers

    def get_queryset(self):
        if not self.request.query_params:
            return self.queryset
        query_list = Shop.objects.select_related('city', 'street').all()
        now_time = datetime.datetime.now().time()
        city = self.request.query_params.get('city', None)
        street = self.request.query_params.get('street', None)
        open = self.request.query_params.get('open', None)
        if city:
            query_list = query_list.filter(street__city_title__title__icontains=city)
        if street:
            query_list = query_list.filter(street__title__icontains=street)
        if open:
            if open == "1":
                query_list = [shop for shop in query_list if time_in_range(shop.time_open, shop.time_close, now_time)]
            elif open == "0":
                query_list = [shop for shop in query_list if time_in_range(shop.time_close, shop.time_open, now_time)]
        return query_list

    def create(self, request, *args, **kwargs):
        query = Street.objects.select_related('city_title').all()
        street = request.data.get('street', None)
        city = request.data.get('city', None)
        if query.filter(pk=street, city_title_id=city):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED, headers=headers)
        super(ShopListCreate, self).create(request, *args, **kwargs)
