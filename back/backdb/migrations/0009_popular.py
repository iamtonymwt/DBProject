# Generated by Django 3.2.9 on 2021-12-30 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backdb', '0008_alter_room_hotel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Popular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=1)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backdb.hotel')),
            ],
        ),
    ]
