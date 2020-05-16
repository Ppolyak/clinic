# Generated by Django 2.0.3 on 2019-04-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190414_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='clients',
            field=models.ManyToManyField(to='accounts.Client'),
        ),
    ]