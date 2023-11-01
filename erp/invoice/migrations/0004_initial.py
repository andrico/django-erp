# Generated by Django 4.2.6 on 2023-10-31 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoice', '0003_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_initial'),
        ('product', '0002_initial'),
        ('customer', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinvoiceitem',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalinvoiceitem',
            name='invoice',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='invoice.invoice'),
        ),
        migrations.AddField(
            model_name='historicalinvoiceitem',
            name='product',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product'),
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='company',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='customer',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='historicalinvoice',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
