# Generated by Django 4.1.6 on 2023-02-16 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=20)),
                ('model_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('model',),
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.productmodel'),
        ),
    ]
