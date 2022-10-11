from .models import Order
from rest_framework.exceptions import NotFound


class DataOrder:
    def __init__(self, date, amount, car_model_id__title, car_model_id__car_make_id__title):
        self.date = date
        self.amount = amount
        self.model = car_model_id__title
        self.make = car_model_id__car_make_id__title
        self.color = None

    def set_color(self, color):
        self.color = color

    @classmethod
    def create_data_order_objects(cls, list_orders, color_order):
        order_data_objects = [cls(**list_order) for list_order in list_orders]
        change_order_data_object = [
            order_data_objects[num].set_color(d['color_id__title']) for num, d in enumerate(color_order)
        ]
        return order_data_objects

    def __str__(self):
        return f'{self.color}, {self.amount}, {self.date}, {self.make}'


class SortedInfoOrder:

    def __init__(self, sort_method):
        self.sort_method = sort_method

    def get_sort_data_order(self):
        if isinstance(self.sort_method, int):
            order_model_make_join, color_order = self._sorting_by_amount()

        elif isinstance(self.sort_method, str):
            order_model_make_join, color_order = self._sorting_by_make()

        else:
            order_model_make_join, color_order = self._sorting_by_amount()

        return order_model_make_join, color_order

    def _sorting_by_amount(self):
        if self.sort_method:
            order_model_make_join = Order.objects.select_related('car_model_id__car_make_id') \
                .order_by('-amount') \
                .values('date', 'amount', 'car_model_id__title', 'car_model_id__car_make_id__title')
            color_order = Order.objects.select_related('color_id').values('color_id__title')
        else:
            order_model_make_join = Order.objects.select_related('car_model_id__car_make_id') \
                .order_by('amount') \
                .values('date', 'amount', 'car_model_id__title', 'car_model_id__car_make_id__title')
            color_order = Order.objects.select_related('color_id').values('color_id__title')

        return order_model_make_join,  color_order

    def _sorting_by_make(self):
        if self.sort_method == 'asc':
            order_model_make_join = Order.objects.select_related('car_model_id__car_make_id') \
                .order_by('-car_model_id__car_make_id__title') \
                .values('date', 'amount', 'car_model_id__title', 'car_model_id__car_make_id__title')
            color_order = Order.objects.select_related('color_id').values('color_id__title')
        elif self.sort_method == 'desc':
            order_model_make_join = Order.objects.select_related('car_model_id__car_make_id') \
                .order_by('car_model_id__car_make_id__title') \
                .values('date', 'amount', 'car_model_id__title', 'car_model_id__car_make_id__title')
            color_order = Order.objects.select_related('color_id').values('color_id__title')
        else:
            raise NotFound('Allowed collations "asc" or "desc"')

        return order_model_make_join, color_order