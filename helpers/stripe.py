import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class Stripe:
    @staticmethod
    def stripe_get_product(obj_id):
        return stripe.Product.retrieve(obj_id)

    @staticmethod
    def stripe_get_price(obj_id):
        return stripe.Price.retrieve(obj_id)

    @staticmethod
    def stripe_customer_get(email: str):
        return stripe.Customer.list(email=email)

    def stripe_customer_create(self, data: dict):
        existing_customer = self.stripe_customer_get(data.get('email'))
        if len(existing_customer.get("data")) > 0:
            return existing_customer.data[0]
        return stripe.Customer.create(**data)

    @staticmethod
    def stripe_create_card(card: dict):
        return stripe.Token.create(card=card)

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
    def stripe_retrive_invoice(invoice_id):
        return stripe.Invoice.retrieve(invoice_id)

    @staticmethod
    def stripe_retrive_intent_id(intent_id):
        return stripe.PaymentIntent.retrieve(intent_id)
