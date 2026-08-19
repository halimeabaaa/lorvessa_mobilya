from django.db import models


class SliderImage(models.Model):
    """Anasayfa slider'da gösterilecek resimler (8 sn otomatik geçiş)."""
    image = models.ImageField(
        'Resim',
        upload_to='slider/',
        blank=True,
        null=True,
        help_text='Anasayfa arka plan görseli. Geniş (yatay) fotoğraf önerilir.',
    )
    title = models.CharField(
        'Başlık',
        max_length=200,
        blank=True,
        help_text='Resmin üzerinde görünen ana başlık.',
    )
    subtitle = models.CharField(
        'Alt yazı',
        max_length=200,
        blank=True,
        help_text='Başlığın altındaki kısa açıklama.',
    )
    order = models.PositiveIntegerField(
        'Sıra',
        default=0,
        help_text='Küçük sayı önce gösterilir (0, 1, 2…).',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Slider resmi'
        verbose_name_plural = 'Slider resimleri'

    def __str__(self):
        return self.title or f'Slider #{self.pk}'


class AboutSection(models.Model):
    """Hakkımızda bölümü - tek kayıt kullanılacak."""
    title = models.CharField(
        'Başlık',
        max_length=200,
        help_text='Bölüm başlığı (örn. Hakkımızda).',
    )
    content = models.TextField(
        'İçerik',
        blank=True,
        help_text='Hakkımızda metni. Paragraflar için Enter kullanabilirsiniz.',
    )
    is_active = models.BooleanField(
        'Aktif',
        default=True,
        help_text='İşaretli değilse sitede gösterilmez.',
    )

    class Meta:
        verbose_name = 'Hakkımızda'
        verbose_name_plural = 'Hakkımızda'

    def __str__(self):
        return self.title


class ServiceItem(models.Model):
    """Yaptığımız işler / hizmetler listesi."""
    title = models.CharField(
        'Başlık',
        max_length=200,
        help_text='Hizmet adı (örn. Dolap Yapımı).',
    )
    description = models.TextField(
        'Açıklama',
        blank=True,
        help_text='Kısa açıklama metni.',
    )
    order = models.PositiveIntegerField(
        'Sıra',
        default=0,
        help_text='Küçük sayı önce gösterilir.',
    )
    is_active = models.BooleanField(
        'Aktif',
        default=True,
        help_text='İşaretli değilse sitede gösterilmez.',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Yaptığımız işler'

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    """Galeri: iş adı, açıklama, resim. 4+4 kutularda, 8'er öğe sayfaları."""
    image = models.ImageField(
        'Resim',
        upload_to='gallery/',
        help_text='Galeri kutusunda gösterilecek fotoğraf.',
    )
    title = models.CharField(
        'Başlık',
        max_length=200,
        help_text='İş veya proje adı.',
    )
    description = models.TextField(
        'Açıklama',
        blank=True,
        help_text='Kısa açıklama; kartta birkaç satır görünür.',
    )
    order = models.PositiveIntegerField(
        'Sıra',
        default=0,
        help_text='Küçük sayı önce gösterilir.',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Galeri öğesi'
        verbose_name_plural = 'Galeri öğeleri'

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    """İletişim bilgileri - adres, telefon, email vb."""
    address = models.CharField(
        'Adres',
        max_length=300,
        blank=True,
        help_text='Tam adres metni.',
    )
    phone = models.CharField(
        'Telefon',
        max_length=50,
        blank=True,
        help_text='Örn. +90 555 000 00 00',
    )
    email = models.EmailField(
        'E-posta',
        blank=True,
        help_text='İletişim e-posta adresi.',
    )
    map_embed_url = models.TextField(
        'Harita embed URL',
        blank=True,
        help_text='Google Maps’ten “Haritayı yerleştir” ile aldığınız iframe src adresi (veya tüm iframe kodu).',
    )
    is_active = models.BooleanField(
        'Aktif',
        default=True,
        help_text='İşaretli değilse sitede gösterilmez.',
    )

    class Meta:
        verbose_name = 'İletişim bilgisi'
        verbose_name_plural = 'İletişim bilgileri'

    def __str__(self):
        return self.email or self.phone or 'İletişim'

    def phone_digits(self):
        return ''.join(c for c in (self.phone or '') if c.isdigit())

    def phone_e164(self):
        """WhatsApp / tel için 90xxxxxxxxxx formatı."""
        digits = self.phone_digits()
        if not digits:
            return '905066791721'
        if digits.startswith('0'):
            digits = '90' + digits[1:]
        elif not digits.startswith('90'):
            digits = '90' + digits
        return digits

    def tel_href(self):
        return f'tel:+{self.phone_e164()}'

    def whatsapp_href(self):
        return f'https://wa.me/{self.phone_e164()}'

    def mailto_href(self):
        if self.email:
            return f'mailto:{self.email}'
        return ''

    def get_map_src(self):
        """Iframe kodundan veya düz URL’den harita src’sini çıkarır."""
        raw = (self.map_embed_url or '').strip()
        if not raw:
            return ''
        if 'src="' in raw:
            start = raw.find('src="') + 5
            end = raw.find('"', start)
            return raw[start:end] if end > start else ''
        if "src='" in raw:
            start = raw.find("src='") + 5
            end = raw.find("'", start)
            return raw[start:end] if end > start else ''
        return raw


class SiteComment(models.Model):
    """Ziyaretçi yorumları — sitede görünür, admin panelinden silinebilir."""
    author_name = models.CharField(
        'Ad Soyad',
        max_length=80,
        help_text='Yorumu yazan kişinin adı.',
    )
    body = models.TextField(
        'Yorum',
        help_text='Yorum metni.',
    )
    created_at = models.DateTimeField(
        'Tarih',
        auto_now_add=True,
    )
    is_visible = models.BooleanField(
        'Sitede göster',
        default=True,
        help_text='İşareti kaldırırsanız yorum silinmeden siteden gizlenir.',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        preview = (self.body or '').strip().replace('\n', ' ')
        if len(preview) > 40:
            preview = preview[:40] + '…'
        return f'{self.author_name}: {preview or "Yorum"}'
