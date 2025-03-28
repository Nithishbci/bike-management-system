import random
from datetime import timedelta

def format_euros(amount):
    return f"€ {amount:,.2f}"

def estimate_service_duration(service_type):
    durations = {
        "general": timedelta(hours=1),
        "home": timedelta(hours=1, minutes=30),
        "accident": timedelta(hours=3),
    }
    return durations.get(service_type.lower(), timedelta(hours=1))

def calculate_service_cost(service_type):
    rates = {
        "general": 50,
        "home": 80,
        "accident": 150,
    }
    return rates.get(service_type.lower(), 50)

def generate_invoice_number():
    return f"INV{random.randint(100000, 999999)}"
