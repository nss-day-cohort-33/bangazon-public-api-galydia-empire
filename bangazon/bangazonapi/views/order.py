"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Customer, PaymentType



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
        fields = ('id', 'url', 'created_date', 'payment_type', 'customer')


class Orders(ViewSet):
    """Orders for Bangazon Galaydia Empire"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized ParkArea instance
        """
        neworder = Order()
        neworder.created_at = request.data["created_at"]
        neworder.paymenttype = PaymentType.objects.get(pk=request.data["paymenttype"])
        customer = Customer.objects.get(user=request.auth.user)
        neworder.customer = customer
        neworder.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order
        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a park area
        Returns:
            Response -- Empty body with 204 status code
        """

        order = Order.objects.get(pk=pk)
        order.payment_type = request.data["payment_type"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


