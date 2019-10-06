"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Customer, PaymentType



class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for orders with two foreign key serializers
    for payment_type and customer to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(),
        view_name="customer-detail",
        many=True,
        required=False,
        lookup_field="pk"
    )
    payment_type = serializers.HyperlinkedRelatedField(
        queryset=PaymentType.objects.all(),
        view_name="payment_type-detail",
        many=True,
        required=False,
        lookup_field="pk"
    )

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_at', 'payment_type', 'customer')



class Orders(ViewSet):
    """Orders for Bangazon Galaydia Empire
    Author: Scott Silver
    Purpose: Allows user to communicate with the Bangazon
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE

    """

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized ParkArea instance
        """
        neworder = Order()
        neworder.created_at = request.data["created_at"]
        neworder.payment_type = PaymentType.objects.get(pk=request.data["payment_type"])
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


