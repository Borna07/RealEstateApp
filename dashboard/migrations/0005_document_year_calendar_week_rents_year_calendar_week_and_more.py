# Generated by Django 4.0.6 on 2023-01-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_document_avg_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='year_calendar_week',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rents',
            name='year_calendar_week',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='avg_price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='avg_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='avg_size',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='highest_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='lowest_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rents',
            name='avg_price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rents',
            name='avg_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rents',
            name='avg_size',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rents',
            name='highest_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rents',
            name='lowest_price_sqrm',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
