# Generated by Django 4.1.6 on 2023-02-16 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_alter_productgroup_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='productfiles')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(default='haict', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='product_files', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='product.product')),
            ],
        ),
    ]