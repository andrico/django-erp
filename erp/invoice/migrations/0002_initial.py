# Generated by Django 4.2.6 on 2023-10-31 22:53

from django.db import migrations
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('invoice', '0001_initial'),
        ('product', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='product',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='product.product'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='company.company'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='customer.customer'),
        ),
    ]
