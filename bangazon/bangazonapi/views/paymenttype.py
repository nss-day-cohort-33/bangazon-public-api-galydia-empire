"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import PaymentType


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
        fields = ('id', 'url', 'merchant_name', 'account_number', 'expiration_date', 'created_at', 'customer_id')


class PaymentTypes(ViewSet):
    """PaymentTypes for Bangazon Galaydia Empire"""

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