# Generated by Django 3.0.5 on 2020-04-07 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200403_0051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='albertheijnproduct',
            options={'ordering': ['-product_id', 'entry_date']},
        ),
    ]
