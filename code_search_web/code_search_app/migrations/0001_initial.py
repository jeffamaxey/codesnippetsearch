# Generated by Django 3.0.8 on 2020-07-16 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QueryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CodeRepository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('commit_hash', models.CharField(blank=True, max_length=256, null=True)),
                ('update_status', models.IntegerField(choices=[(0, 'In Progress'), (1, 'Finished'), (2, 'Error')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('languages', models.ManyToManyField(to='code_search_app.CodeLanguage')),
            ],
        ),
        migrations.CreateModel(
            name='CodeDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048)),
                ('path', models.CharField(max_length=2048)),
                ('identifier', models.CharField(max_length=2048)),
                ('code', models.TextField()),
                ('code_hash', models.CharField(max_length=64)),
                ('embedded_row_index', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_search_app.CodeLanguage')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_search_app.CodeRepository')),
            ],
        ),
        migrations.AddIndex(
            model_name='codedocument',
            index=models.Index(fields=['repository', 'language', 'embedded_row_index'], name='code_search_reposit_e8e783_idx'),
        ),
        migrations.AddIndex(
            model_name='codedocument',
            index=models.Index(fields=['code_hash'], name='code_search_code_ha_732501_idx'),
        ),
    ]