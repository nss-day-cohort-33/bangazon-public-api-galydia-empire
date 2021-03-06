"""View module for handling requests about product types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    # Author: Sam Birky
    # Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
    # Methods: GET POST PUT DELETE

    """JSON serializer for product types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='ProductType',
            lookup_field='pk'
        )
        fields = ('id', 'url', 'name', 'product_set')
        depth = 2

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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product Type instance
        """
        product_type = ProductType()
        product_type.name = request.data["name"]
        product_type.save()

        serializer = ProductTypeSerializer(product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized product type instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product type

        Returns:
            Response -- Empty body with 204 status code
        """
        product_type = ProductType.objects.get(pk=pk)
        product_type.name = request.data["name"]
        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)