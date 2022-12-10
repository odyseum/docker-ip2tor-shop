# Generated by Django 4.1.3 on 2022-11-28 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lnpurchase', '0001_initial'),
        ('lninvoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderinvoice',
            name='po',
            field=models.ForeignKey(editable=False, help_text='The originating Purchase Order.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ln_invoices', to='lnpurchase.purchaseorder', verbose_name='Purchase Order'),
        ),
    ]
