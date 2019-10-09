"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Product, Customer, ProductType


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description',
                  'quantity', 'location', 'created_at', 'customer', 'product_type')


class Products(ViewSet):
    """Products for Bangazon Galaydia Empire"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        new_product = Product()
        new_product.name = request.data["name"]
        new_product.customer = Customer.objects.get(user=request.auth.user)
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.created_at = request.data["created_at"]
        new_product.product_type = ProductType.objects.get(pk=request.data["product_type"])
        new_product.location = request.data["location"]
        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            single_product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(single_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT requests for an individual product to be edited

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.quantity = request.data["quantity"]
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_twenty(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        category = self.request.query_params.get('category', None)
        quantity = self.request.query_params.get('quantity', None)
        if category is not None:
            products = products.filter(product_category__id=category)

        if quantity is not None:
            quantity = int(quantity)
            length = len(products)
            new_products = list()
            count = 0
            for product in products:
                count += 1
                if count - 1 + quantity >= length:
                    new_products.append(product)
                    if count == length:
                        products = new_products
                        break

        serializer = ProductSerializer(
            products, many=True, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)