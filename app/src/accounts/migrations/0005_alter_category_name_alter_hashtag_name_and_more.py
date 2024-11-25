# Generated by Django 5.1.3 on 2024-11-18 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_category_hashtag_keyword_remove_product_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='accounts.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='products', to='accounts.hashtag'),
        ),
        migrations.AlterField(
            model_name='product',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='products', to='accounts.keyword'),
        ),
        migrations.AlterField(
            model_name='product',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='accounts.merchant'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='promotions', to='accounts.category'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='promotions', to='accounts.hashtag'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='promotions', to='accounts.keyword'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='accounts.product'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='accounts.service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='services', to='accounts.category'),
        ),
        migrations.AlterField(
            model_name='service',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='services', to='accounts.hashtag'),
        ),
        migrations.AlterField(
            model_name='service',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='services', to='accounts.keyword'),
        ),
        migrations.AlterField(
            model_name='service',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='accounts.merchant'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
