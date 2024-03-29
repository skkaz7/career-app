# Generated by Django 4.1.2 on 2022-10-06 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('link', models.CharField(max_length=64)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True)),
                ('estimated_time', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('difficulty', models.IntegerField(choices=[(1, 'Łatwe'), (2, 'średnie'), (3, 'Trudne')])),
                ('category', models.CharField(max_length=64)),
                ('slug', models.CharField(max_length=64, unique=True)),
                ('deadline', models.DateField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='career_app.task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_app.project')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_app.status')),
                ('website', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='career_app.website')),
            ],
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('received', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
                ('type_of_contract', models.IntegerField(choices=[(1, 'Umowa o pracę'), (2, 'B2B'), (3, 'Umowa zlecenie'), (4, 'Umowa o dzieło')])),
                ('benefits', models.TextField()),
                ('requirements', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_app.company')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_app.website')),
            ],
        ),
    ]
