# Generated by Django 4.1.7 on 2023-09-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_reviews_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_reviews',
            name='review_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]