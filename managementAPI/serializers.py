from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import User,Event,Ticket


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['username','password','role']


    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 80)
    password = serializers.CharField(max_length = 155,write_only = True)
    access_token = serializers.CharField(max_length = 255,read_only = True)
    refresh_token = serializers.CharField(max_length = 255,read_only = True)

    class Meta:
        model = User
        fields = ['username','password','access_token','refresh_token']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request,username=username,password=password)

        if not user:
            raise AuthenticationFailed({"message":(_("Invalid username or password"))})   
        
        tokens = user.tokens()
        return {
            'username':username,
            'access_token':tokens.get('access'),
            'refresh_token':tokens.get('refresh'),
        }


class EventManagementSerializer(serializers.ModelSerializer):
    tickets_sold = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['id','name','date','total_tickets','tickets_sold']

    
class TicketPurchaseSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    event = serializers.CharField(read_only=True)
    purchase_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['user','event','quantity','purchase_date']

    def validate(self, attrs):
        quantity = attrs['quantity']
        id = self.context['id']
        self.event = Event.objects.get(id=id)

        '''
        validating for quantity of purchase ticket should not equal to or less than zero
        '''
        if quantity<=0:
            raise serializers.ValidationError(_("Cannot buy less than one ticket"))

        '''
        validating for ticket quantity requested does not exceed available tickets
        '''
        if not quantity+self.event.tickets_sold <= self.event.total_tickets:
            raise serializers.ValidationError(_("purchasing for a non-existent event"))
        
        return attrs
    
    # Perform multiple database operations within a single transaction
    @transaction.atomic()
    def create(self, validated_data):
        quantity = validated_data['quantity']
        request = self.context.get('request')
        '''
        creating ticket for requested quantity as the above validation is successfull
        '''
        ticket = Ticket.objects.create(user=request.user,event=self.event,quantity=quantity)
        
        # updating ticket_sold attribute in particular event
        self.event.tickets_sold = self.event.tickets_sold + quantity
        self.event.save()
        return ticket