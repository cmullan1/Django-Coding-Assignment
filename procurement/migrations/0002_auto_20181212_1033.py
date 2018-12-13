# Generated by Django 2.1.2 on 2018-12-12 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('representative_name', models.CharField(max_length=255)),
                ('representative_email', models.EmailField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='representative_email',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='representative_name',
        ),
        migrations.AddField(
            model_name='representative',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Supplier'),
        ),
    ]