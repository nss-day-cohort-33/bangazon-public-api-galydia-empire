"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import PaymentType, Customer


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='PaymentType',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name', 'account_number',
                  'expiration_date', 'created_at', 'customer')
        depth = 1


class PaymentTypes(ViewSet):
    """PaymentTypes for Bangazon Galaydia Empire"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        payment_type = PaymentType()
        payment_type.merchant_name = request.data["merchant_name"]
        payment_type.account_number = request.data["account_number"]
        payment_type.expiration_date = request.data["expiration_date"]
        payment_type.customer = Customer.objects.get(user=request.auth.user)
        payment_type.save()

        serializer = PaymentTypeSerializer(payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment type instance
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a payment type

        Returns:
            Response -- Empty body with 204 status code
        """
        payment_type = PaymentType.objects.get(pk=pk)
        payment_type.merchant_name = request.data["merchant_name"]
        payment_type.account_number = request.data["account_number"]
        payment_type.expiration_date = request.data["expiration_date"]
        payment_type.created_at = request.data["created_at"]
        user = User.objects.get(pk=request.data["user_id"])
        payment_type.customer = Customer.objects.get(user=user)
        payment_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types resource

        Returns:
            Response -- JSON serialized list of payment_type
        """
        payment_types = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(
            payment_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)