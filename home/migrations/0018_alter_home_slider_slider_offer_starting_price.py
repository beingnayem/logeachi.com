# Generated by Django 4.1.7 on 2023-09-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_banner_created_at_event_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home_slider',
            name='slider_offer_starting_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True),
        ),
    ]