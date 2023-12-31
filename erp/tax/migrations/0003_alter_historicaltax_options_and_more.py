# Generated by Django 4.2.6 on 2023-11-01 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicaltax',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Impuesto', 'verbose_name_plural': 'historical Impuestos'},
        ),
        migrations.AlterModelOptions(
            name='historicaltaxgroup',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Grupo de Impuestos', 'verbose_name_plural': 'historical Grupos de Impuestos'},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Impuesto', 'verbose_name_plural': 'Impuestos'},
        ),
        migrations.AlterModelOptions(
            name='taxgroup',
            options={'verbose_name': 'Grupo de Impuestos', 'verbose_name_plural': 'Grupos de Impuestos'},
        ),
        migrations.AlterField(
            model_name='historicaltax',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='historicaltax',
            name='percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Porcentaje'),
        ),
        migrations.AlterField(
            model_name='historicaltax',
            name='subtract',
            field=models.BooleanField(default=False, verbose_name='Restar'),
        ),
        migrations.AlterField(
            model_name='historicaltaxgroup',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Porcentaje'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='subtract',
            field=models.BooleanField(default=False, verbose_name='Restar'),
        ),
        migrations.AlterField(
            model_name='taxgroup',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='taxgroup',
            name='taxes',
            field=models.ManyToManyField(related_name='groups', to='tax.tax', verbose_name='Impuestos'),
        ),
    ]
