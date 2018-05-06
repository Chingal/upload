import django_filters
from apps.tickets.models import Ticket

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'status': ['exact', ],
            'created_at': ['lte', 'gte'],
        }