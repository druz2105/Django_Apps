import json

from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.stripe import Stripe
from .models import SubscriptionPlan
from .serializers import SubscriptionPlansListSerializers, SubscriptionPlansCreateSerializers
from ..users.services import UserServices, UserSubscriptionService

stripe = Stripe()


class SubscriptionPlansListView(ListAPIView):
    serializer_class = SubscriptionPlansListSerializers
    queryset = SubscriptionPlan.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})


class CreateSubscriptionView(CreateAPIView):
    user_service = UserServices()
    serializer_class = SubscriptionPlansCreateSerializers

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            card_details: dict = request.data.get('card_details')
            price_id: str = request.data.get('price_id')
            prod_id: str = request.data.get('prod_id')
            user: UserServices.model = request.user
            subscription = self.user_service.get_user_subscription(user)
            if subscription:
                subscription_data = stripe.stripe_subscription_get(subscription.subscription_id)
                if subscription_data.status in ['active', 'trialing']:
                    return Response(status=status.HTTP_200_OK,
                                    data={"subscription": subscription_data,
                                          'subscription_id': subscription.subscription_id,
                                          "price_id": price_id, "prod_id": prod_id, "message": "Already subscribed!"})
            if not user.customer_id:
                customer = stripe.stripe_customer_create(
                    {'email': user.email, 'name': f'{user.first_name} {user.last_name}'})
                user.customer_id = customer.id
                user.save()
            customer_id = user.customer_id
            card_token = stripe.stripe_create_card(card_details)
            card_source = stripe.stripe_creat_source(card_token.id, customer_id)
            stripe.stripe_customer_card_update(customer_id, card_source.id)
            subscription = stripe.stripe_subscription_create(customer_id=customer_id, items=[{"price": price_id}])
            if subscription.status in ['active', 'trialing']:
                return Response(status=status.HTTP_200_OK,
                                data={"subscription": subscription, 'subscription_id': subscription.id,
                                      "price_id": price_id, "prod_id": prod_id, "message": "Successfully subscribed!"})
            else:
                invoice_id = subscription.latest_invoice
                invoice = stripe.stripe_retrieve_invoice(invoice_id)
                intent_id = invoice.payment_intent
                intent = stripe.stripe_retrieve_intent_id(intent_id)
                return Response(status=status.HTTP_200_OK,
                                data={"intent": intent, "subscription_id": subscription.id, "price_id": price_id,
                                      "prod_id": prod_id, "message": "Validate payment to get ahead!"})


class ValidateSubscriptionAPIView(CreateAPIView):
    user_service = UserServices()
    user_sub_service = UserSubscriptionService()

    def post(self, request, **kwargs):
        subscription_id: str = request.data.get('subscription_id')
        price_id: str = request.data.get('price_id')
        prod_id: str = request.data.get('prod_id')
        check_subscription = stripe.stripe_subscription_get(subscription_id)
        user: UserServices.model = request.user
        self.user_sub_service.create_or_update(
            {
                'user': user,
                'subscription_id': subscription_id,
                'status': check_subscription.status,
                "price_id": price_id,
                "prod_id": prod_id
            })
        return Response(status=status.HTTP_200_OK, data={"subscription_valid": check_subscription.status})


class VerifySubscriptionAPIView(RetrieveAPIView):
    user_service = UserServices()
    user_sub_service = UserSubscriptionService()

    def retrieve(self, request, *args, **kwargs):
        user: UserServices.model = request.user
        subscription = self.user_service.get_user_subscription(user)
        if subscription and subscription.status in ['active', 'trailing']:
            return Response(status=status.HTTP_200_OK, data={"subscription_status": True})
        return Response(status=status.HTTP_200_OK, data={"subscription_status": False})
