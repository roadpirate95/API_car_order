from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .pagination import MyLimitOffsetPagination
from .helpers import  SortedInfoOrder
from .models import CarModel, CarMake, Color, Order
from .serializers import OrderModelSerializer, ColorSerializer, CarModelSerializer, CarMakeSerializer,\
    OrderInfoSerializer, ColorInfoSerializer, CarMakeInfoSerializer
from rest_framework.decorators import action


class OrderViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD для модели Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class ColorViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD для модели Color.
    Также API для получения списка цветов с количестовом заказанных авто одного цвета /color_and_amount/
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = MyLimitOffsetPagination

    @action(detail=False)
    def color_and_amount(self, request):
        color_orders_join = Color.objects.prefetch_related(Prefetch('order_color', to_attr='prefetched_order'))
        page = self.paginate_queryset(color_orders_join)
        if page is not None:
            serializer = ColorInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ColorInfoSerializer(color_orders_join, many=True)
        return Response(serializer.data)


class CarModelViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD для модели CarModel.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarMakeViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD для модели CarMake.
    Также API для получения списка марок с количестовом заказанных авто каждой марки /make_and_amount/
    """
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    pagination_class = MyLimitOffsetPagination

    @action(detail=False)
    def make_and_amount(self, request):
        make_order_join = CarMake.objects.prefetch_related(
            Prefetch('car_models', queryset=CarModel.objects.prefetch_related('order_model')))
        page = self.paginate_queryset(make_order_join)
        if page is not None:
            serializer = CarMakeInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CarMakeInfoSerializer(make_order_join, many=True)
        return Response(serializer.data)


class OrderInfo(APIView, MyLimitOffsetPagination):
    """
    API для отображения списка заказв и сортировки по возрастанию количествa авто в заказе, используйте /order_info/,
    по убыванию /order_info/{любая цифра}/. Для отображения списка заказа и сортировки по маркам авто используйте
    order_info/{asc}/ или order_info/{desc}/
    """

    def get(self, request, *args, **kwargs):
        order_color_model_make_join = SortedInfoOrder(kwargs.get('sort')).get_sort_data_order()

        page = self.paginate_queryset(order_color_model_make_join, request)
        if page is not None:
            serializer = OrderInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderInfoSerializer(order_color_model_make_join, many=True)
        return Response(serializer.data)
