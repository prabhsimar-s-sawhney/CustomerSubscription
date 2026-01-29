from apps.base.models import Customer    


def get_all_customers():
    return Customer.objects.all()

def get_active_customers():
    return Customer.objects.filter(status="active")

def get_customer_by_id(customer_id):
    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None

def get_customer_by_email(email):
    try:
        return Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return None

def get_customer_by_phone(phone_number):
    try:
        return Customer.objects.get(phone_number=phone_number)
    except Customer.DoesNotExist:
        return None