import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class CardDetails:
    def __init__(self, exp_month: int, exp_year: int, last4: str, id: str, **kwargs):
        self.card_id = id
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.last4 = last4

    def get_data(self):
        return {'last4': self.last4, 'exp_month': self.exp_month, 'exp_year': self.exp_year, 'card_id': self.card_id}


class SubscriptionDetails:
    def __init__(self, id: str, current_period_start: int, current_period_end: int, status: str, **kwargs):
        self.sub_id = id
        self.current_period_start = current_period_start
        self.current_period_end = current_period_end
        self.status = status

    def get_data(self):
        return {'sub_id': self.sub_id, 'current_period_start': self.current_period_start,
                'current_period_end': self.current_period_end, 'status': self.status}


class ProductDetails:
    def __init__(self, id: str, name: str, **kwargs):
        self.prod_id = id
        self.name = name

    def get_data(self):
        return {'prod_id': self.prod_id, 'name': self.name}


class PriceDetails:
    def __init__(self, id: str, currency: str, unit_amount: int, recurring: dict, **kwargs):
        self.price_id = id
        self.currency = currency
        self.unit_amount = unit_amount
        self.recurring = recurring

    def get_data(self):
        return {'price_id': self.price_id, 'currency': self.currency, "unit_amount": self.unit_amount,
                "recurring": self.recurring}


class Stripe:
    @staticmethod
    def stripe_get_product(prod_id):
        return stripe.Product.retrieve(prod_id)

    @staticmethod
    def stripe_get_price(price_id):
        return stripe.Price.retrieve(price_id)

    @staticmethod
    def stripe_customers_get(email: str):
        return stripe.Customer.list(email=email)

    @staticmethod
    def stripe_customers_retrieve(customer_id: str):
        return stripe.Customer.retrieve(customer_id)

    def stripe_customer_create(self, data: dict):
        existing_customer = self.stripe_customers_get(data.get('email'))
        if len(existing_customer.get("data")) > 0:
            return existing_customer.data[0]
        return stripe.Customer.create(**data)

    @staticmethod
    def stripe_customer_card_update(cus_id: str, card_id: str):
        return stripe.Customer.modify(cus_id, **{"default_source": card_id})

    @staticmethod
    def stripe_create_card(card: dict):
        return stripe.Token.create(card=card)

    @staticmethod
    def stripe_retrieve_card(customer_id: str, card_id: str):
        return stripe.Customer.retrieve_source(customer_id, card_id)

    @staticmethod
    def stripe_creat_source(card_source: str, customer_id: str):
        return stripe.Customer.create_source(customer_id, source=card_source)

    @staticmethod
    def stripe_subscription_get(sub_id: str):
        return stripe.Subscription.retrieve(sub_id)

    @staticmethod
    def stripe_subscription_create(customer_id: str, items: list):
        return stripe.Subscription.create(
            customer=customer_id,
            items=items,
        )

    @staticmethod
    def stripe_retrieve_invoice(invoice_id):
        return stripe.Invoice.retrieve(invoice_id)

    @staticmethod
    def stripe_retrieve_intent_id(intent_id):
        return stripe.PaymentIntent.retrieve(intent_id)
