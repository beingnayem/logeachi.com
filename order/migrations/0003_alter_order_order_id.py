# Generated by Django 4.1.7 on 2023-09-26 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='A32lXuiHgh', editable=False, max_length=10, unique=True),
        ),
    ]