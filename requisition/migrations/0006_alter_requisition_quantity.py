# Generated by Django 4.1.2 on 2022-10-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0005_alter_requisition_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]