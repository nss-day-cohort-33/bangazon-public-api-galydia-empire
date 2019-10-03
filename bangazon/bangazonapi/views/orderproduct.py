"""View module for handling requests about orderproducts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import OrderProduct


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orderProducts

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderProduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product')


class OrderProducts(ViewSet):
    """OrderProducts for Bangazon Galaydia Empire"""

    def list(self, request):
        """Handle GET requests to orderProducts resource

        Returns:
            Response -- JSON serialized list of orderProducts
        """
        order_products = OrderProduct.objects.all()
        serializer = OrderProductSerializer(
            order_products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)