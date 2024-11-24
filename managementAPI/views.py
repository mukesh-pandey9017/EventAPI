from rest_framework.generics import GenericAPIView,CreateAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminRole,AuthenticateUserOnly
from rest_framework import status
from .models import User, Event
from .serializers import UserRegistrationSerializer, UserLoginSerializer, EventManagementSerializer, TicketPurchaseSerializer

# Create your views here.

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer


class UserLoginView(GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class EventManagementView(ListCreateAPIView):
    serializer_class = EventManagementSerializer
    queryset = Event.objects.all()

    '''
    applying IsAdminRole custom permission and IsAuthenticated permission
    through get_permissions methods
    '''
    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsAdminRole()]
        return [IsAuthenticated()]


class TicketPurchaseView(CreateAPIView):
    serializer_class = TicketPurchaseSerializer
    permission_classes = [AuthenticateUserOnly] # AuthenticateUserOnly is a custom permission
    lookup_field = 'id'
    
    def get_serializer_context(self):
        return {'id':self.kwargs['id'],'request':self.request}