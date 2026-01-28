from datetime import timedelta, timezone
from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import TimeStamped
from .enum_schemas import (
    customer_status, duration_units, duration_units_in_days,
    transaction_types, transaction_reasons, subscription_status
)

class Customer(TimeStamped):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=10, choices=customer_status, default='active')

class Service(TimeStamped):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):

        if not self.description:
            self.description = f"{self.name} service."

        return super().save(force_insert, force_update, using, update_fields)

class ServiceTier(TimeStamped):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    service = models.ForeignKey(Service, related_name="tiers", on_delete=models.CASCADE)
    rank = models.IntegerField(blank=False, help_text="Rank of the tier within the service. Lower number indicates higher tier.")

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):

        if not self.description:
            self.description = f"{self.name} tier for {self.service.name} service."

        return super().save(force_insert, force_update, using, update_fields)

class Plan(TimeStamped):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    credits = models.IntegerField(blank=False, help_text="Number of credits per duration of subscription")
    duration_uom = models.CharField(max_length=10, choices=duration_units, blank=False)
    service_tier = models.ForeignKey(ServiceTier, related_name="plans", on_delete=models.CASCADE)

    @property
    def is_upgradable(self):
        tier = self.service_tier

        max_rank = ServiceTier.objects.filter(
            service=tier.service
        ).aggregate(models.Max("rank"))["rank__max"]

        return tier.rank < max_rank

    @property
    def is_downgradable(self):
        tier = self.service_tier

        min_rank = ServiceTier.objects.filter(
            service=tier.service
        ).aggregate(models.Min("rank"))["rank__min"]

        return tier.rank > min_rank

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        
        if not self.description:
            self.description = f"{self.name} plan for {self.service.name} service."

        return super().save(force_insert, force_update, using, update_fields)

class CustomerPlanSubscription(TimeStamped):
    customer = models.ForeignKey(Customer, related_name="subscriptions", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name="subscriptions", on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=subscription_status)

    @property
    def current_balance(self):

        total_credit = self.credit_ledgers.filter(transaction_type='credit', 
                                                  transaction_date__lte=timezone.now(), 
                                                  credit_expiry_date__gte=timezone.now()).aggregate(models.Sum('amount')
                                                )['amount__sum'] or 0
        
        total_debit = self.credit_ledgers.filter(transaction_type='debit', 
                                                 transaction_date__lte=timezone.now()).aggregate(models.Sum('amount')
                                                )['amount__sum'] or 0
        return total_credit - total_debit

    def plan_already_exists(self):

        service = self.plan.service_tier.service
        plan_exists = CustomerPlanSubscription.objects.filter(
            customer=self.customer,
            plan__service_tier__service=service,
            status='active'
        ).exclude(pk=self.pk).exists()

        return plan_exists

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.plan_already_exists():
            raise ValidationError(
                "Customer already has a plan for this service"
            )

        return super().save(force_insert, force_update, using, update_fields)

class CreditLedger(TimeStamped):
    subscription = models.ForeignKey(CustomerPlanSubscription, related_name="credit_ledgers", on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False)
    transaction_type = models.CharField(max_length=10, choices=transaction_types, blank=False)
    transaction_reason = models.CharField(max_length=10, choices=transaction_reasons, blank=False)
    transaction_date = models.DateTimeField(blank=False)
    credit_expiry_date = models.DateTimeField(blank=True, null=True)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):

        if self.transaction_type == "credit" and not self.credit_expiry_date:
            self.credit_expiry_date = timezone.now() + timedelta(days=duration_units_in_days.get(self.subscription.plan.duration_uom, 30))

        if not self.transaction_date:
            self.transaction_date = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)