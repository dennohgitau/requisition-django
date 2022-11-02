# Generated by Django 4.1.2 on 2022-10-24 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateField(default=django.utils.timezone.now)),
                ('department', models.CharField(max_length=50)),
                ('item', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('seller_name', models.CharField(max_length=50)),
                ('seller_address', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_date'],
            },
        ),
    ]
