import logging
from apps.base.models import Customer

logger = logging.getLogger(__name__)

def create_customer(data):
    try:
        customer = Customer(**data)
        customer.save()
        return customer
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        return None