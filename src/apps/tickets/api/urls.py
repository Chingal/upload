from django.urls import path
from .views import *

urlpatterns = [
    path('tickets/', TicketList.as_view(), name=TicketList.name),
    path('tickets/<int:pk>/', TicketDetail.as_view(), name=TicketDetail.name),
    path('files/', FileList.as_view(), name=FileList.name),
    path('files/<int:pk>/', FileDetail.as_view(), name=FileDetail.name),
    path('', ApiRoot.as_view(), name=ApiRoot.name),
]