# Generated by Django 4.1.7 on 2023-03-31 03:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usersubscription_price_id_usersubscription_prod_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usersubscription',
            unique_together={('user', 'subscription_id')},
        ),
    ]
