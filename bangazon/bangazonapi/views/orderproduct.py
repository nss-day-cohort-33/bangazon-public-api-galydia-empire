"""View module for handling requests about orderproducts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import OrderProduct, Product, Order


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):

    # Author: Sam Birky
    # Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries.
    # Methods: GET POST DELETE
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
        depth = 1


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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized order products instance
        """
        order_product = OrderProduct()
        order_product.order = Order.objects.get(pk=request.data["order"])
        order_product.product = Product.objects.get(pk=request.data["product"])
        order_product.save()

        serializer = OrderProductSerializer(
            order_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order product

        Returns:
            Response -- JSON serialized payment type instance
        """
        try:
            single_order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                single_order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a payment type

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     order_product = OrderProduct.objects.get(pk=pk)
    #     order_product.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
