"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Customer, PaymentType, OrderProduct



class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for orders to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_at', 'payment_type', 'customer')
        depth = 1


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

        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        current_customer = Customer.objects.get(pk=request.user.id)
        order = Order.objects.filter(customer=current_customer, payment_type=None)

        if order.exists():
            order_item.order = order[0]
        else:
            new_order = Order()
            new_order.customer = current_customer
            new_order.save()
            order_item.order = new_order
        
        order_item.save()

        serializer = OrderSerializer(order_item, context={'request': request})
# At this point, the model instance has been translated into Python native datatypes.
# To finalize the serialization process we render the data into json.
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
            Response -- JSON serialized list of orders with customer
        """
        orders = Order.objects.all()
        customer = Customer.objects.get(pk=request.user.id)

        # Sends back all closed orders for the order history view, or the single open order to display in cart view
        cart = self.request.query_params.get('cart', None)
        orders = orders.filter(customer_id=customer)
        print("orders", orders)
        if cart is not None:
            orders = orders.filter(payment=None).get()
            print("orders filtered", orders)
            serializer = OrderSerializer(
                orders, many=False, context={'request': request}
              )
        else:
            serializer = OrderSerializer(
                orders, many=True, context={'request': request}
              )
        return Response(serializer.data)
