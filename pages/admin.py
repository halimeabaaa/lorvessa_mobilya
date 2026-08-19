from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    SliderImage,
    AboutSection,
    ServiceItem,
    GalleryItem,
    ContactInfo,
    SiteComment,
)


admin.site.site_header = 'Lorvessa Mobilya Yönetim'
admin.site.site_title = 'Lorvessa Mobilya'
admin.site.index_title = 'Site Yönetimi'


class SingletonModelAdmin(admin.ModelAdmin):
    """Tek kayıtlı içerikler için: ikinci kayıt eklemeyi engeller, tek kayıt varsa düzenlemeye gider."""

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = self.model.objects.first()
        if obj is not None:
            url = reverse(
                f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
                args=[obj.pk],
            )
            return redirect(url)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('preview', 'title', 'subtitle', 'order')
    list_display_links = ('preview', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'subtitle')
    ordering = ('order',)
    list_per_page = 20

    fieldsets = (
        ('Görsel', {
            'description': 'Anasayfada tam ekran gösterilecek resmi seçin. Geniş, yatay fotoğraflar en iyi sonucu verir.',
            'fields': ('image',),
        }),
        ('Metinler', {
            'description': 'Başlık ve alt yazı resmin üzerinde görünür. İsterseniz boş bırakabilirsiniz.',
            'fields': ('title', 'subtitle'),
        }),
        ('Sıralama', {
            'description': 'Küçük sayı önce gösterilir. Örn. 0, 1, 2…',
            'fields': ('order',),
        }),
    )

    @admin.display(description='Önizleme')
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="lorenza-thumb" alt="" />',
                obj.image.url,
            )
        return mark_safe('<span class="lorenza-thumb-placeholder">Yok</span>')


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonModelAdmin):
    list_display = ('title', 'is_active', 'short_content')
    list_display_links = ('title',)
    list_editable = ('is_active',)

    fieldsets = (
        (None, {
            'description': 'Sitede tek bir “Hakkımızda” metni kullanılır. Aktif kaydı işaretleyin.',
            'fields': ('title', 'content', 'is_active'),
        }),
    )

    @admin.display(description='Özet')
    def short_content(self, obj):
        text = (obj.content or '').strip()
        if len(text) > 80:
            return text[:80] + '…'
        return text or '—'


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'short_description')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)

    fieldsets = (
        (None, {
            'description': '“Yaptığımız İşler” bölümünde listelenen hizmetler.',
            'fields': ('title', 'description', 'order', 'is_active'),
        }),
    )

    @admin.display(description='Açıklama')
    def short_description(self, obj):
        text = (obj.description or '').strip()
        if len(text) > 70:
            return text[:70] + '…'
        return text or '—'


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('preview', 'title', 'order', 'short_description')
    list_display_links = ('preview', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    list_per_page = 24

    fieldsets = (
        ('Görsel', {
            'description': 'Galeri kutusunda görünecek fotoğrafı yükleyin.',
            'fields': ('image',),
        }),
        ('Bilgiler', {
            'fields': ('title', 'description'),
        }),
        ('Sıralama', {
            'description': 'Öğeler 8’erli sayfalar halinde gösterilir. Sıra numarası görünüm sırasını belirler.',
            'fields': ('order',),
        }),
    )

    @admin.display(description='Önizleme')
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="lorenza-thumb" alt="" />',
                obj.image.url,
            )
        return mark_safe('<span class="lorenza-thumb-placeholder">Yok</span>')

    @admin.display(description='Açıklama')
    def short_description(self, obj):
        text = (obj.description or '').strip()
        if len(text) > 60:
            return text[:60] + '…'
        return text or '—'


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonModelAdmin):
    list_display = ('address', 'phone', 'email', 'has_map', 'is_active')
    list_display_links = ('address', 'email')
    list_editable = ('is_active',)

    fieldsets = (
        ('İletişim', {
            'description': 'İletişim bölümünde gösterilecek bilgiler. Genelde tek kayıt yeterlidir.',
            'fields': ('address', 'phone', 'email', 'is_active'),
        }),
        ('Harita', {
            'description': 'Google Maps → Paylaş → Haritayı yerleştir. Iframe kodunun tamamını veya yalnızca src URL’sini yapıştırabilirsiniz.',
            'fields': ('map_embed_url',),
        }),
    )

    @admin.display(description='Harita', boolean=True)
    def has_map(self, obj):
        return bool(obj.get_map_src())


@admin.register(SiteComment)
class SiteCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'short_body', 'created_at', 'is_visible')
    list_display_links = ('author_name', 'short_body')
    list_filter = ('is_visible', 'created_at')
    list_editable = ('is_visible',)
    search_fields = ('author_name', 'body')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    actions = ('hide_comments', 'show_comments')

    fieldsets = (
        (None, {
            'description': 'Uygunsuz yorumları buradan silebilir veya “Sitede göster” işaretini kaldırarak gizleyebilirsiniz.',
            'fields': ('author_name', 'body', 'is_visible', 'created_at'),
        }),
    )

    @admin.display(description='Yorum')
    def short_body(self, obj):
        text = (obj.body or '').strip().replace('\n', ' ')
        if len(text) > 70:
            return text[:70] + '…'
        return text or '—'

    @admin.action(description='Seçilen yorumları siteden gizle')
    def hide_comments(self, request, queryset):
        queryset.update(is_visible=False)

    @admin.action(description='Seçilen yorumları sitede göster')
    def show_comments(self, request, queryset):
        queryset.update(is_visible=True)
