# Customer Status to maintain current availability
customer_status = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
]

#Subscription Status to maintain active subscriptions
subscription_status = [
    ('active', 'Active'),
    ('cancelled', 'Cancelled'),
    ('upgraded', 'Upgraded'),
    ('downgraded', 'Downgraded'),
]

# Duration Units
duration_units = [
    ('months', 'Months'),
    ('years', 'Years'),
]

#Duration units into days
duration_units_in_days = {
    'months': 30,
    'years': 365,
}

# Transaction Types for ledgers
transaction_types = [
    ('credit', 'Credit'),
    ('debit', 'Debit'),
]

# Transaction Reasons for ledgers
transaction_reasons = [
    ('allocation', 'Allocation'),
    ('usage', 'Usage'),
    ('refund', 'Refund'),
    ('adjustment', 'Adjustment'),
    ('bonus', 'Bonus'),
]