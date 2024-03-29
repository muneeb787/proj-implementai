# Generated by Django 5.0.1 on 2024-02-09 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=300)),
                ('vapi_call_id', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('AC', 'Active'), ('PD', 'Pending')], default='PD', editable=False, max_length=2)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
