# Generated by Django 2.0.3 on 2019-04-14 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190328_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='clients',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.Client'),
        ),
    ]
