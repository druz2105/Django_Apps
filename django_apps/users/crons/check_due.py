import os

from sendgrid.helpers.mail import Mail
from sendgrid.sendgrid import SendGridAPIClient

from django_apps.users.models import UserSubscription
from helpers.custom_stripe import CustomStripe

sendgrid_client = SendGridAPIClient(api_key=os.getenv('SENDGRID_KEY'))
stripe = CustomStripe()


def check_subscription():
    try:
        # with open('../../../logs/logs.txt') as file:
        #     file.write("Cron run at every five minutes")
        #     file.close()
        user_subs = UserSubscription.objects.all()
        print(len(user_subs))
        for sub in user_subs:
            subscription = stripe.stripe_subscription_get(sub.subscription_id)
            if subscription.status == "past_due":
                sub.status = subscription.status
                sub.save()
                invoice_id = subscription.latest_invoice
                invoice = stripe.stripe_retrieve_invoice(invoice_id)
                message = Mail(
                    from_email="dhruvilp012@gmail.com",
                    to_emails=sub.user.email)
                message.dynamic_template_data = {
                    'customerName': sub.user.full_name,
                    'intentLink': invoice.hosted_invoice_url,
                    'invoicePDF': invoice.invoice_pdf
                }
                message.template_id = os.getenv("OVERDUE_TEMPLATE")
                sendgrid_client.send(message)
            else:
                sub.status = subscription.status
                sub.save()

    except Exception as e:
        print(e)
        # with open('../../../logs/err_logs.txt') as file:
        #     file.write(e.__str__())
        #     file.close()
