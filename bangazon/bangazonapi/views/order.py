"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'payment_type', 'created', 'completed')


class Orders(ViewSet):
    """Orders for Bangazon Galaydia Empire"""

    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)