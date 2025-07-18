# Generated by Django 5.2.1 on 2025-06-02 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('fiscal_year', models.CharField(blank=True, max_length=10, null=True)),
                ('batch_number', models.IntegerField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('total_training_hours', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('organizer', models.CharField(default='Unknown', max_length=255)),
                ('training_type', models.CharField(choices=[('ইন-হাউজ/অভ্যন্তরীণ', 'ইন-হাউজ/অভ্যন্তরীণ'), ('স্থানীয়', 'স্থানীয়'), ('বৈদেশিক', 'বৈদেশিক')], default='ইন-হাউজ/অভ্যন্তরীণ', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('office_address', models.TextField()),
                ('gender', models.CharField(max_length=10)),
                ('contact', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('batch_number', models.IntegerField()),
                ('Official_ID', models.CharField(max_length=255)),
                ('total_training_hours', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.batch')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.training')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialClearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_spent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance_receiver', models.CharField(max_length=255)),
                ('adjustment_info', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.batch')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.training')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='dashboard.training'),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file_path', models.FileField(upload_to='attachments/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.batch')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.training')),
            ],
        ),
    ]
