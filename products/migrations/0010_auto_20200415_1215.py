# Generated by Django 3.0.5 on 2020-04-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200414_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albertheijnproductdetails',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
