from rest_framework import serializers
from helpers.custom_stripe import CustomStripe
from .models import SubscriptionPlan

stripe = CustomStripe()


class SubscriptionPlansListSerializers(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()
    price_data = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'product_data', 'price_data')

    # noinspection PyMethodMayBeStatic
    def get_product_data(self, instance):
        return stripe.stripe_get_product(instance.product_id)

    # noinspection PyMethodMayBeStatic
    def get_price_data(self, instance):
        return stripe.stripe_get_price(instance.price_id)


class CardSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=16, min_length=16, required=True)
    exp_month = serializers.CharField(max_length=2, min_length=1, required=True)
    exp_year = serializers.CharField(max_length=2, min_length=1, required=True)
    cvc = serializers.CharField(max_length=4, min_length=3, required=True)


class SubscriptionPlansCreateSerializers(serializers.Serializer):
    card_details = serializers.CharField(required=True)
    price_id = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)

    class Meta:
        fields = ('card_details', 'user_id', 'price_id')
