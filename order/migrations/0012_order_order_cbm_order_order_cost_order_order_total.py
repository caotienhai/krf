# Generated by Django 4.1.6 on 2023-02-24 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_delete_orderfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_cbm',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='order_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(default=0),
        ),
    ]