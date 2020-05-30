import django_filters
from django_filters import DateFilter
from .models import Order

class OrderFilter(django_filters.FilterSet):
	class Meta:
		model = Order
		fields = ['product', 'status']
