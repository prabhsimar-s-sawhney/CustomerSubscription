from django.db import models
from apps.core.models import TimeStamped

class Customer(TimeStamped):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
