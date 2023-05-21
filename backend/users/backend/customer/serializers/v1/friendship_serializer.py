from rest_framework import serializers

from customer.models import CustomerUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'
