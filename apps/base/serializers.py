from rest_framework import serializers
from apps.base.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
    
    def validate_email(self, value):
        """Ensure email uniqueness during creation and updates"""
        if self.instance:
            # During update, exclude current instance
            if Customer.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        else:
            # During creation
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        return value
    
    def validate_phone_number(self, value):
        """Ensure phone number uniqueness during creation and updates"""
        if value is None:
            return value
            
        if self.instance:
            # During update, exclude current instance
            if Customer.objects.exclude(pk=self.instance.pk).filter(phone_number=value).exists():
                raise serializers.ValidationError("A customer with this phone number already exists.")
        else:
            # During creation
            if Customer.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError("A customer with this phone number already exists.")
        return value