from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import DataOrder, SortedInfoOrder
from .models import CarModel, CarMake, Color, Order
from .serializers import OrderModelSerializer, ColorSerializer, CarModelSerializer, CarMakeSerializer,\
    OrderInfoSerializer, ColorInfoSerializer, CarMakeInfoSerializer
from rest_framework.decorators import action


class OrderViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class ColorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @action(detail=False)
    def color_and_amount(self, request):
        color_orders_join = Color.objects.prefetch_related(Prefetch('order_color', to_attr='prefetched_order'))
        serializer = ColorInfoSerializer(color_orders_join, many=True)

        return Response(serializer.data)



class CarModelViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarMakeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer

    @action(detail=False)
    def make_and_amount(self, request):
        make_order_join = CarMake.objects.prefetch_related(
            Prefetch('car_models', queryset=CarModel.objects.prefetch_related('order_model')))

        serializer = CarMakeInfoSerializer(make_order_join, many=True)

        return Response(serializer.data)


class OrderInfo(APIView):

    def get(self, request, *args, **kwargs):

        order_model_make_join, color_order = SortedInfoOrder(kwargs.get('sort')).get_sort_data_order()
        order_data_objects = DataOrder.create_data_order_objects(list_orders=order_model_make_join,
                                                                 color_order=color_order)

        serializer = OrderInfoSerializer(order_data_objects, many=True)

        return Response(serializer.data)
