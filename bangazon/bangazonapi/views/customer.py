"""View module for handling requests about customers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer

"""
Author: Scott Silver
Purpose: Allows user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
Methods: GET, PUT, POST, DELETE
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for users

    Arguments:
        serializers.HyperlinkedModelSerializer

    """
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name',
        'last_name', 'email', 'date_joined', 'is_active')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    """JSON serializer for customers

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
        )
        fields = ('id', 'url', 'user', 'address', 'phone_number')
        depth = 1


class Customers(ViewSet):
    """Customers for Bangazon Galaydia Empire"""

    def retrieve(self, request, pk=None):

        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a customer
        Author: Scott Silver
        Purpose: Allows a user to communicate with the Bangazon database to update  customer's 'is_active property
        Method:  PUT
        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=pk)
        customer.user.is_active = False
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to customers resource

        Returns:
            Response -- JSON serialized list of customers
        """
        customers = Customer.objects.all()
        serializer = CustomerSerializer(
            customers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
