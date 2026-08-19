from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_serviceitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(help_text='Yorumu yazan kişinin adı.', max_length=80, verbose_name='Ad Soyad')),
                ('body', models.TextField(help_text='Yorum metni.', verbose_name='Yorum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Tarih')),
                ('is_visible', models.BooleanField(default=True, help_text='İşareti kaldırırsanız yorum silinmeden siteden gizlenir.', verbose_name='Sitede göster')),
            ],
            options={
                'verbose_name': 'Yorum',
                'verbose_name_plural': 'Yorumlar',
                'ordering': ['-created_at'],
            },
        ),
    ]
