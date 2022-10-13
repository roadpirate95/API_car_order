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

    make = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['amount', 'date', 'make', 'model', 'color']

    def get_model(self, obj):
        return obj['car_model_id__title']

    def get_color(self, obj):
        return obj['color_id__title']

    def get_make(self, obj):
        return obj['car_model_id__car_make_id__title']


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
