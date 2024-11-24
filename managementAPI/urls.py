from django.urls import path
from .views import UserRegistrationView,UserLoginView,EventManagementView,TicketPurchaseView

urlpatterns = [
    path("api/register/",UserRegistrationView.as_view(),name='register'),
    path("api/login/",UserLoginView.as_view(),name='login'),
    path("api/events/",EventManagementView.as_view(),name='event'),
    path("api/events/<int:id>/purchase/",TicketPurchaseView.as_view(),name='ticket'),
]