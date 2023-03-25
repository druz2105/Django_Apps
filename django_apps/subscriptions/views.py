import json

from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.stripe import Stripe
from .models import SubscriptionPlan
from .serializers import SubscriptionPlansListSerializers, SubscriptionPlansCreateSerializers
from ..users.services import UserServices, UserSubscriptionService

stripe = Stripe()


class SubscriptionPlansListView(ListAPIView):
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
    serializer_class = SubscriptionPlansCreateSerializers

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            card_details: dict = request.data.get('card_details')
            price_id: str = request.data.get('price_id')
            user: UserServices.model = self.user_service.get_user_object_id(request.data.get('user_id'))
            if not user.customer_id:
                customer = stripe.stripe_customer_create(
                    {'email': user.email, 'name': f'{user.first_name} {user.last_name}'})
                user.customer_id = customer.id
                user.save()
            customer_id = user.customer_id
            card_source = stripe.stripe_create_card(card_details)
            stripe.stripe_creat_source(card_source.id, customer_id)
            subscription = stripe.stripe_subscription_create(customer_id=customer_id, items=[{"price": price_id}])
            if subscription.status in ['active', 'trialing']:
                return Response(status=status.HTTP_200_OK,
                                data={"subscription": subscription, 'subscription_id': subscription.id})
            else:
                invoice_id = subscription.latest_invoice
                invoice = stripe.stripe_retrive_invoice(invoice_id)
                intent_id = invoice.payment_intent
                intent = stripe.stripe_retrive_intent_id(intent_id)
                return Response(status=status.HTTP_200_OK, data={"intent": intent, "subscription_id": subscription.id})


class CheckSubscriptionAPIView(CreateAPIView):
    user_service = UserServices()
    user_sub_service = UserSubscriptionService()
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        subscription_id = request.data.get('subscription_id')
        check_subscription = stripe.stripe_subscription_get(subscription_id)
        user: UserServices.model = self.user_service.get_user_object_id(request.data.get('user_id'))
        if check_subscription.status == 'active':
            self.user_sub_service.create(
                {'user': user, 'subscription_id': subscription_id, 'status': check_subscription.status})
        return Response(status=status.HTTP_200_OK, data={"subscription_valid": check_subscription.status})
