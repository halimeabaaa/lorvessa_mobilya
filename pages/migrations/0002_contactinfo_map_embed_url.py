# Generated manually for ContactInfo.map_embed_url

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='map_embed_url',
            field=models.TextField(
                blank=True,
                help_text='Google Maps’ten “Haritayı yerleştir” ile aldığınız iframe src adresi (veya tüm iframe kodu).',
                verbose_name='Harita embed URL',
            ),
        ),
    ]
