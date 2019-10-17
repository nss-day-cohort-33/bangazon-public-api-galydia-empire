"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Customer, PaymentType, OrderProduct, Product
from rest_framework.decorators import action
from .product import ProductSerializer


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
    Author: Scott Silver & Matthew Caldwell
    Purpose: Allows user to communicate with the Bangazon
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """

    @action(methods=['get'], detail=False)
    def current(self, request):
        customer = Customer.objects.get(user=request.auth.user)
        try:
            my_order = Order.objects.filter(
                customer=customer, payment_type_id=None).get()
            serializer = OrderSerializer(
                my_order, many=False, context={'request': request})
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized ParkArea instance
        """
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        current_customer = Customer.objects.get(pk=request.user.id)
        order = Order.objects.filter(
            customer=current_customer, payment_type=None)

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
        customer = Customer.objects.get(user=request.auth.user)

        try:
            my_order = Order.objects.filter(
                customer=customer, payment_type_id=None)
            serializer = OrderSerializer(
                my_order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area
        Returns:
            Response -- Empty body with 204 status code
        """

        order = Order.objects.get(pk=pk)
        order.payment_type_id = request.data["payment_type"]
        products_on_order = Product.objects.filter(cart__order=order)
        order.save()

        for product in products_on_order:
            product.quantity -= 1
            product.save()

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

    # Example request:
    #   http://localhost:8000/orders/cart
    @action(methods=['get'], detail=False)
    def cart(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(
                customer=current_user, payment_type=None)
            products_on_order = Product.objects.filter(cart__order=open_order)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            products_on_order, many=True, context={'request': request})
        return Response(serializer.data)

    # Created by Joy
    # To filter completed orders (orders with an existing payment type)
    # Example request:  http://localhost:8000/orders/completed
    @action(methods=['get'], detail=False)
    def completed(self, request):
        customer = Customer.objects.get(user=request.auth.user)
        try:
            my_order = Order.objects.filter(
                customer=customer, payment_type_id=True).get()
            serializer = OrderSerializer(
                my_order, many=False, context={'request': request})
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
