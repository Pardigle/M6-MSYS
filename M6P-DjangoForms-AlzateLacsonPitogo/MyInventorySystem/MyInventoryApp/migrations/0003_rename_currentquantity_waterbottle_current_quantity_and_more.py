# Generated by Django 5.1.6 on 2025-03-25 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyInventoryApp', '0002_supplier_city_supplier_country_supplier_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='waterbottle',
            old_name='currentQuantity',
            new_name='current_quantity',
        ),
        migrations.RenameField(
            model_name='waterbottle',
            old_name='mouthSize',
            new_name='mouth_size',
        ),
        migrations.RenameField(
            model_name='waterbottle',
            old_name='suppliers',
            new_name='supplier',
        ),
    ]
