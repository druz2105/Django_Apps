from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from stripe.error import CardError

from helpers.custom_stripe import CustomStripe, CardDetails, PriceDetails, ProductDetails, SubscriptionDetails
from .serializers import (UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserDetailSerializer,
                          ProfileImageSerializer, ChangePasswordSerializer)
from .services import UserServices

stripe = CustomStripe()


# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CustomObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomRefreshJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailUpdateView(RetrieveUpdateDestroyAPIView):
    service = UserServices()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', "PATCH"]:
            return UserUpdateSerializer
        else:
            return UserDetailSerializer

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        return super().update(request, args, kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.delete()


class ProfileImageCreateView(CreateAPIView):
    serializer_class = ProfileImageSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.get_object().check_password(serializer.data["old_password"]):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.get_object().set_password(serializer.data["password"])
            self.get_object().save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStripeDetailsAPI(ListAPIView):
    service = UserServices()

    def list(self, request, *args, **kwargs):
        data = {}
        user: UserServices.model = request.user
        customer_id = user.customer_id
        customer = stripe.stripe_customers_retrieve(customer_id)
        card_details = stripe.stripe_retrieve_card(customer_id, customer.default_source)
        data['card_details'] = CardDetails(**card_details).get_data()
        user_subscription = self.service.get_user_subscription(user)
        if user_subscription:
            subscription = stripe.stripe_subscription_get(user_subscription.subscription_id)
            print(subscription)
            data['subscription'] = SubscriptionDetails(**subscription).get_data()
        else:
            data['subscription'] = {}
        product = stripe.stripe_get_product(user_subscription.prod_id)
        price = stripe.stripe_get_price(user_subscription.price_id)
        data['product'] = ProductDetails(**product).get_data()
        data['price'] = PriceDetails(**price).get_data()
        return Response(status=status.HTTP_200_OK, data=data)


class UserCardUpdateAPI(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            user: UserServices.model = request.user
            customer_id = user.customer_id
            card_token = stripe.stripe_create_card(request.data)
            card_source = stripe.stripe_creat_source(card_token.id, customer_id)
            stripe.stripe_customer_card_update(customer_id, card_source.id)
            return Response(status=status.HTTP_200_OK, data=request.data)
        except CardError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Card Declined"})
