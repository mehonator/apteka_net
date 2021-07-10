# Generated by Django 3.2.4 on 2021-07-08 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delevery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Доставка',
                'verbose_name_plural': 'Доставки',
            },
        ),
        migrations.CreateModel(
            name='UnitOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True, verbose_name='Название подразделения')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('STAFF', 'Staff'), ('head_of_pharmacy', 'Head_of_pharmacy'), ('admin', 'Admin')], default='STAFF', max_length=20)),
                ('units_organizations', models.ManyToManyField(related_name='profiles_staff', to='logistics.UnitOrganization', verbose_name='Профили сотрудников')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='профиль')),
            ],
            options={
                'verbose_name': 'Профиль сотрудника',
                'verbose_name_plural': 'Профили сотрудников',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Название позиции доставки')),
                ('count', models.FloatField(verbose_name='Количество позиции доставки')),
                ('delevery', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='logistics.delevery')),
                ('unit_organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='logistics.unitorganization')),
            ],
            options={
                'verbose_name': 'Торговая позиция',
                'verbose_name_plural': 'Торговые позиции',
            },
        ),
        migrations.AddField(
            model_name='delevery',
            name='from_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='from_unit', to='logistics.unitorganization', verbose_name='Пункт доставки'),
        ),
        migrations.AddField(
            model_name='delevery',
            name='to_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='to_unit', to='logistics.unitorganization', verbose_name='Пункт отправки'),
        ),
    ]
