from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from apps.base.serializers import CustomerSerializer
from apps.base.selectors import get_active_customers, get_customer_by_id

class CustomerListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        customers = get_active_customers()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'email' in str(e):
                    return Response(
                        {"email": ["A customer with this email already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif 'phone_number' in str(e):
                    return Response(
                        {"phone_number": ["A customer with this phone number already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"detail": "A customer with these details already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CustomerDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        customer = get_customer_by_id(kwargs.get("customer_id"))
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        customer = get_customer_by_id(kwargs.get("customer_id"))
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError as e:
                if 'email' in str(e):
                    return Response(
                        {"email": ["A customer with this email already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif 'phone_number' in str(e):
                    return Response(
                        {"phone_number": ["A customer with this phone number already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"detail": "A customer with these details already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        customer = get_customer_by_id(kwargs.get("customer_id"))
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        customer = get_customer_by_id(kwargs.get("customer_id"))
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError as e:
                if 'email' in str(e):
                    return Response(
                        {"email": ["A customer with this email already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif 'phone_number' in str(e):
                    return Response(
                        {"phone_number": ["A customer with this phone number already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"detail": "A customer with these details already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
