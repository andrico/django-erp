# Generated by Django 4.2.6 on 2023-11-01 19:07

from django.db import migrations
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_historicallistprice_company_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalproduct',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Producto', 'verbose_name_plural': 'historical Productos'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterField(
            model_name='historicalproductimage',
            name='product',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='historicalproductoption',
            name='product',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='historicalproductprice',
            name='product',
            field=simple_history.models.HistoricForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='product',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='product',
            field=simple_history.models.HistoricForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='product.product', verbose_name='Producto'),
        ),
    ]
