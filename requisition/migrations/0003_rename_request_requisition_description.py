# Generated by Django 4.1.2 on 2022-10-24 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0002_requisition_request_alter_requisition_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requisition',
            old_name='request',
            new_name='description',
        ),
    ]