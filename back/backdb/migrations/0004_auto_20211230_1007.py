# Generated by Django 3.2.9 on 2021-12-30 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backdb', '0003_auto_20211229_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='date',
            field=models.DateField(default='2021-12-29'),
        ),
        migrations.AddField(
            model_name='room',
            name='platform_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backdb.platform'),
        ),
        migrations.AddField(
            model_name='room',
            name='sum',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='business',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backdb.business'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='score',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='score_count',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='url',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='score',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='room',
            name='count',
            field=models.IntegerField(default=3),
        ),
    ]
