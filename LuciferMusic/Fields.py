from rest_framework import serializers
from django.db.models import Manager
from django.db.models.query import QuerySet

class LatestRelatedField(serializers.RelatedField):

    def __init__(self, order_field=None ,**kwargs):
        assert order_field is not None, 'The `order_field` argument is required.'
        self.order_field = order_field
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, (QuerySet, Manager)):
            if queryset.count() > 0:
                result_obj = queryset.order_by("-"+self.order_field)[0]
                queryset = queryset.none()
                queryset = queryset | result_obj
        return queryset
