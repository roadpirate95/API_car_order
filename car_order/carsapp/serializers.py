from rest_framework import serializers
from .models import CarModel, CarMake, Color, Order


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = '__all__'


class CarMakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarMake
        fields = '__all__'


class OrderInfoSerializer(serializers.Serializer):

    amount = serializers.IntegerField()
    make = serializers.CharField(max_length=250)
    model = serializers.CharField(max_length=250)
    date = serializers.DateField()
    color = serializers.CharField(max_length=250)


class ColorInfoSerializer(serializers.ModelSerializer):
    amount_car = serializers.SerializerMethodField()

    class Meta:
        model = Color
        fields = ['title', 'amount_car']

    def get_amount_car(self, obj):
        return sum([order.amount for order in obj.prefetched_order])


class CarMakeInfoSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = CarMake
        fields = ['title', 'amount']

    def get_amount(self, obj):
        list_amount = []
        for car_model in obj.car_models.all():
            for order in car_model.order_model.all():
                list_amount.append(order.amount)
        return sum(list_amount)
