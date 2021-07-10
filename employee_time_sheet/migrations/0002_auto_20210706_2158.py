# Generated by Django 3.2.4 on 2021-07-06 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logistics', '0005_auto_20210706_1946'),
        ('employee_time_sheet', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TabelUchetaRabochegoVremeniT12',
            new_name='Table',
        ),
        migrations.RenameModel(
            old_name='RowOfTabelUchetaRabochegoVremeni',
            new_name='Row',
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(blank=True, null=True, verbose_name='День')),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_time_sheet.row')),
            ],
        ),
    ]