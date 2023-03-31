from django_apps.users.models import UserSubscription
from helpers.stripe import Stripe

stripe = Stripe()


def check_subscription():
    try:
        with open('../../../logs/logs.txt') as file:
            file.write("Cron run at every five minutes")
            file.close()
        user_subs = UserSubscription.objects.all()
        for sub in user_subs:
            subscription = stripe.stripe_subscription_get(sub.subscription_id)
            sub.status = subscription.status
            sub.save()
    except Exception as e:
        with open('../../../logs/err_logs.txt') as file:
            file.write(e.__str__())
            file.close()
