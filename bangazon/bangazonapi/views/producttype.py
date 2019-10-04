"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='ProductType',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class ProductTypes(ViewSet):
    """Product types for Bangazon Galaydia Empire"""

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        product_types = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            product_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)