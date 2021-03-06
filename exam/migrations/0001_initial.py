# Generated by Django 3.1.4 on 2021-01-09 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import exam.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=120, verbose_name='Jawaban')),
                ('answer_image', models.ImageField(blank=True, null=True, upload_to=exam.models.answer_directory_path, verbose_name='Gambar Jawaban')),
                ('is_right', models.BooleanField(default=False, verbose_name='Benar')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passcode', models.CharField(max_length=20, verbose_name='Passcode')),
                ('exam_title', models.CharField(max_length=100, verbose_name='Judul Ujian')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=120, verbose_name='Pertanyaan')),
                ('question_image', models.ImageField(blank=True, null=True, upload_to=exam.models.question_directory_path, verbose_name='Gambar Pertanyaan')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.exam')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(null=True, verbose_name='Score')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exam.answer')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exam.exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exam.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.question'),
        ),
    ]
