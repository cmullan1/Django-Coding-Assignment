# Generated by Django 2.1.2 on 2018-12-12 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0002_auto_20181212_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='representative',
            options={'ordering': ('representative_name',)},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ('name',)},
        ),
    ]