# Generated by Django 3.2.6 on 2021-10-11 16:09

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('enrollment_no', models.IntegerField(default=0)),
                ('User_name', models.CharField(max_length=100)),
                ('admin', models.BooleanField(default=False)),
                ('enabled', models.BooleanField(default=True)),
                ('email', models.CharField(max_length=254, null=True)),
                ('profile', models.FileField(max_length=254, null=True, upload_to=None)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Card_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Project_name', models.CharField(max_length=100)),
                ('wiki', ckeditor.fields.RichTextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('admins', models.ManyToManyField(related_name='admins_Project', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('List_name', models.CharField(max_length=100)),
                ('Project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listsassociated', to='api.project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('Comment', models.CharField(max_length=100)),
                ('Card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentsofcards', to='api.card')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mycomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='List',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cardsoflist', to='api.list'),
        ),
        migrations.AddField(
            model_name='card',
            name='assigned',
            field=models.ManyToManyField(related_name='mycards', to=settings.AUTH_USER_MODEL),
        ),
    ]
