# Generated by Django 4.1.2 on 2022-10-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0011_requisition_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
