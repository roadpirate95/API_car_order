from .models import Order
from rest_framework.exceptions import NotFound
from django.db import models


class DataOrder(models.query.QuerySet):
    def __init__(self, date, amount, car_model_id__title, car_model_id__car_make_id__title):
        self.date = date
        self.amount = amount
        self.model_auto = car_model_id__title
        self.make = car_model_id__car_make_id__title
        self.color = None
        super(DataOrder, self).__init__()

    def set_color(self, color):
        self.color = color

    @classmethod
    def create_data_order_objects(cls, list_orders, color_order):
        order_data_objects = [cls(**list_order) for list_order in list_orders]
        _ = [
            order_data_objects[num].set_color(d['color_id__title']) for num, d in enumerate(color_order)
        ]
        return order_data_objects

    def __str__(self):
        return f'{self.color}, {self.amount}, {self.date}, {self.make}'


class SortedInfoOrder:
    """Класс для сортировки списка заказов """

    def __init__(self, sort_method):
        self.sort_method = sort_method

    def get_sort_data_order(self):
        """Функция проверет атрибут self.sort_method и в зависимости от него определяет тип сортировки"""

        if isinstance(self.sort_method, int):
            order_model_make_join, color_order = self._sorting_by_amount()

        elif isinstance(self.sort_method, str):
            order_model_make_join, color_order = self._sorting_by_make()

        else:
            order_model_make_join, color_order = self._sorting_by_amount()

        return order_model_make_join, color_order

    def _sorting_by_amount(self):
        """Получает данные из базы и сортирует по количеству машин в заказе"""

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

        return order_model_make_join, color_order

    def _sorting_by_make(self):
        """Получает данные из базы и сортирует по марке машин в заказе"""

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
