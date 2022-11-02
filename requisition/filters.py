import django_filters
from . models import Requisition

class RequisitionFilter(django_filters.FilterSet):

    class Meta:
        model = Requisition
        fields = [
            'sent_date',
            'owner',
            'department',
        ]