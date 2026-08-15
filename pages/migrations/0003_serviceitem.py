from django.db import migrations, models


SERVICES = [
    (
        'Özel Ölçü Mobilya Üretimi',
        'Kişiye özel tasarlanan tüm mobilyaların üretimi.',
    ),
    (
        'Dolap Yapımı',
        'Mutfak, banyo, gardırop, vestiyer, TV ünitesi, kiler ve diğer dolap sistemleri.',
    ),
    (
        'İç Mekân Ahşap Uygulamaları',
        'Duvar panelleri, lambiri, lake panel, dekoratif çıta, tavan ve ahşap kaplamalar.',
    ),
    (
        'Ofis ve Ticari Alan Mobilyaları',
        'Ofis, mağaza, restoran, otel, klinik ve kafe mobilyaları.',
    ),
    (
        'Kapı ve Ahşap Doğrama İşleri',
        'Oda kapıları, sürgülü kapılar, ahşap doğramalar ve özel kapı sistemleri.',
    ),
    (
        'Restorasyon ve Tadilat',
        'Eski mobilyaların yenilenmesi, tamiri, boya, cila ve onarım işlemleri.',
    ),
    (
        'Montaj ve Kurulum Hizmetleri',
        'Üretilen mobilyaların yerinde kurulumu ve montajı.',
    ),
    (
        'Ahşap Merdiven ve Dekoratif Yapılar',
        'Merdivenler, korkuluklar, pergolalar, deck ve dekoratif ahşap yapılar.',
    ),
    (
        'CNC Kesim ve Ahşap İşleme',
        'CNC oyma, kesim, özel desen ve hassas üretim hizmetleri.',
    ),
    (
        'Projelendirme ve Tasarım',
        'Keşif, ölçülendirme, 3D modelleme, iç mimari danışmanlık ve üretim planlaması.',
    ),
]


def seed_services(apps, schema_editor):
    ServiceItem = apps.get_model('pages', 'ServiceItem')
    if ServiceItem.objects.exists():
        return
    for i, (title, description) in enumerate(SERVICES):
        ServiceItem.objects.create(
            title=title,
            description=description,
            order=i,
            is_active=True,
        )


def unseed_services(apps, schema_editor):
    ServiceItem = apps.get_model('pages', 'ServiceItem')
    titles = [t for t, _ in SERVICES]
    ServiceItem.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_contactinfo_map_embed_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Hizmet adı (örn. Dolap Yapımı).', max_length=200, verbose_name='Başlık')),
                ('description', models.TextField(blank=True, help_text='Kısa açıklama metni.', verbose_name='Açıklama')),
                ('order', models.PositiveIntegerField(default=0, help_text='Küçük sayı önce gösterilir.', verbose_name='Sıra')),
                ('is_active', models.BooleanField(default=True, help_text='İşaretli değilse sitede gösterilmez.', verbose_name='Aktif')),
            ],
            options={
                'verbose_name': 'Hizmet',
                'verbose_name_plural': 'Yaptığımız işler',
                'ordering': ['order'],
            },
        ),
        migrations.RunPython(seed_services, unseed_services),
    ]
