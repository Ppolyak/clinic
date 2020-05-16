# Generated by Django 2.0.3 on 2019-04-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_auto_20190416_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('client_from', models.ManyToManyField(to='accounts.Client')),
                ('doctor_to', models.ManyToManyField(to='accounts.Doctor')),
            ],
        ),
    ]