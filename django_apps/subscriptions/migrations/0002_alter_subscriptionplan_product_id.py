# Generated by Django 4.1.7 on 2023-03-24 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='product_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]