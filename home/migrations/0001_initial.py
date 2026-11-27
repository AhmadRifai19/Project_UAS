from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='EvaluasiSusu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph', models.FloatField()),
                ('suhu', models.FloatField()),
                ('rasa', models.CharField(max_length=5)),
                ('bau', models.CharField(max_length=5)),
                ('lemak', models.CharField(max_length=5)),
                ('kekeruhan', models.CharField(max_length=5)),
                ('hasil', models.CharField(max_length=10)),
                ('skor', models.FloatField()),
                ('dibuat_pada', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Evaluasi Susu',
                'verbose_name_plural': 'Evaluasi Susu',
                'ordering': ['-dibuat_pada'],
            },
        ),
    ]