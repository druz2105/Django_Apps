from django.db import models


class SubscriptionPlan(models.Model):
    product_id = models.CharField(max_length=50, null=True, blank=True)
    price_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.product_id
