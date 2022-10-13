from .models import Order
from rest_framework.exceptions import NotFound


class SortedInfoOrder:
    """Класс для получения и сортировки списка заказов """

    def __init__(self, sort_method):
        self.sort_method = sort_method

    def get_sort_data_order(self):
        if isinstance(self.sort_method, int):
            order_model_make_join_sort = self._sorting_by_amount()

        elif isinstance(self.sort_method, str):
            order_model_make_join_sort = self._sorting_by_make()

        else:
            order_model_make_join_sort = self._sorting_by_amount()

        return order_model_make_join_sort

    def _sorting_by_amount(self):
        if self.sort_method:
            order_model_make_join = Order.objects.select_related('color_id'). \
                select_related('car_model_id'). \
                select_related('car_model_id__car_make_id'). \
                order_by('-amount'). \
                values('date', 'amount', 'color_id__title', 'car_model_id__title', 'car_model_id__car_make_id__title')
        else:
            order_model_make_join = Order.objects.select_related('color_id'). \
                select_related('car_model_id'). \
                select_related('car_model_id__car_make_id'). \
                order_by('amount'). \
                values('date', 'amount', 'color_id__title', 'car_model_id__title', 'car_model_id__car_make_id__title')

        return order_model_make_join

    def _sorting_by_make(self):
        if self.sort_method == 'asc':
            order_model_make_join = Order.objects.select_related('color_id'). \
                select_related('car_model_id'). \
                select_related('car_model_id__car_make_id'). \
                order_by('car_model_id__car_make_id__title'). \
                values('date', 'amount', 'color_id__title', 'car_model_id__title', 'car_model_id__car_make_id__title')
        elif self.sort_method == 'desc':
            order_model_make_join = Order.objects.select_related('color_id'). \
                select_related('car_model_id'). \
                select_related('car_model_id__car_make_id'). \
                order_by('-car_model_id__car_make_id__title'). \
                values('date', 'amount', 'color_id__title', 'car_model_id__title', 'car_model_id__car_make_id__title')
        else:
            raise NotFound()

        return order_model_make_join
