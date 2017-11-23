# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 16:59
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.TextField(choices=[('mini-mlh-event', 'Mini MLH Event'), ('general-workshop', 'General Workshop'), ('company-workshop', 'Company Workshop'), ('speaker-session', 'Speaker Session'), ('fireside-chats', 'Fireside Chats'), ('open-source-event', 'General Open Source Event'), ('activity', 'General Activity')])),
                ('name', models.CharField(max_length=50)),
                ('tagline', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=350)),
                ('speaker_details', django.contrib.postgres.fields.jsonb.JSONField()),
                ('location', models.CharField(max_length=150)),
                ('giveaway', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=150)),
                ('version', models.PositiveIntegerField(default=1)),
                ('description', models.TextField()),
                ('logo', models.TextField(null=True)),
                ('hackathon_type', models.TextField(choices=[('high-school', 'High School Hackathon'), ('university', 'University Level Hackathon'), ('corporate', 'Corporate Level Hackathon'), ('other', 'Other')])),
                ('location', models.CharField(max_length=350)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('shipping_address', models.CharField(max_length=350)),
                ('travel_reimbursements', models.TextField()),
                ('university_name', models.CharField(max_length=350, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('social_links', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bus_routes', django.contrib.postgres.fields.jsonb.JSONField()),
                ('timetable', django.contrib.postgres.fields.jsonb.JSONField()),
                ('sponsors', django.contrib.postgres.fields.jsonb.JSONField()),
                ('judges', django.contrib.postgres.fields.jsonb.JSONField()),
                ('speakers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('prizes', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Hacker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.TextField(choices=[('organiser', 'Organiser'), ('participant', 'Participant'), ('volunteer', 'Volunteer'), ('mentor', 'Mentor')])),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Hackathon')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating_for', models.TextField(choices=[('hackathon', 'Rating for Hackathon'), ('event', 'Rating for Event at Hackathon')])),
                ('rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Event')),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Hackathon')),
                ('hacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Hacker')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth0_id', models.TextField(unique=True)),
                ('username', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('gender', models.TextField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number format: '+999999999'. Max 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('level_of_study', models.TextField(choices=[('high-school', 'High School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('doctoral', 'PhD'), ('other', 'Other')])),
                ('major_of_study', models.CharField(max_length=150)),
                ('school_last_attended', models.CharField(max_length=150, null=True)),
                ('graduation_year', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1950)])),
                ('graduation_month', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('tshirt_size', models.TextField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')])),
                ('country', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('zipcode', models.PositiveIntegerField(null=True)),
                ('street_address', models.CharField(max_length=350, null=True)),
                ('birthday', models.DateField()),
                ('social_links', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('dietary_restrictions', models.TextField(choices=[('halal', 'Halal'), ('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('gluten-free', 'Gluten-free'), ('lactose-intolerant', 'Lactose Intolerant'), ('kosher', 'Kosher'), ('none', 'None')])),
                ('special_accommodations', models.TextField(null=True)),
                ('technical_interests', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('technologies', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('about_me', models.TextField(null=True)),
                ('sponsors_interested_in', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('prizes_interested_in', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('experience_points', models.IntegerField(default=0)),
                ('badges_links', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('sticker_book_links', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
            ],
        ),
        migrations.AddField(
            model_name='hacker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='hackathon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Hackathon'),
        ),
        migrations.AddField(
            model_name='event',
            name='hackers',
            field=models.ManyToManyField(to='api.Hacker'),
        ),
    ]
