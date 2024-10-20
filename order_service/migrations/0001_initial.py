# Generated by Django 5.1.2 on 2024-10-19 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('customer_id', models.CharField(max_length=100)),
                ('order_date', models.CharField(max_length=10)),
                ('shipped_date', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('price', models.CharField(max_length=10)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_service.order')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
    ]
