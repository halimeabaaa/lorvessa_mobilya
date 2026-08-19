from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
import json
import time

from .models import (
    SliderImage,
    AboutSection,
    ServiceItem,
    GalleryItem,
    ContactInfo,
    SiteComment,
)
from .forms import SiteCommentForm
from .seo import build_json_ld, default_seo
from .sitemaps import StaticViewSitemap


def home(request):
    """Tek sayfa: Anasayfa, Hakkımızda, Hizmetler, Galeri, İletişim."""
    gallery_items = list(
        GalleryItem.objects.only('id', 'image', 'title', 'description', 'order').order_by('order')
    )
    batch_size = 8
    gallery_batches = [
        gallery_items[i : i + batch_size]
        for i in range(0, len(gallery_items), batch_size)
    ]
    if not gallery_batches and gallery_items:
        gallery_batches = [gallery_items]

    services = list(
        ServiceItem.objects.filter(is_active=True).only('id', 'title', 'description', 'order')
    )
    about = AboutSection.objects.filter(is_active=True).only('id', 'title', 'content').first()
    contact = ContactInfo.objects.filter(is_active=True).first()
    slider_images = list(
        SliderImage.objects.only('id', 'image', 'title', 'subtitle', 'order').order_by('order')
    )
    seo = default_seo()
    json_ld = build_json_ld(
        contact=contact,
        services=services,
        about=about,
        request=request,
    )

    # LCP için ilk slider WebP
    lcp_image = ''
    if slider_images and slider_images[0].image:
        from .image_utils import best_full_url
        lcp_image = request.build_absolute_uri(best_full_url(slider_images[0].image))

    context = {
        'slider_images': slider_images,
        'about': about,
        'services': services,
        'gallery_items': gallery_items,
        'gallery_batches': gallery_batches,
        'contact': contact,
        'comments': SiteComment.objects.filter(is_visible=True).only(
            'id', 'author_name', 'body', 'created_at'
        )[:50],
        'comment_form': SiteCommentForm(),
        'seo': seo,
        'json_ld': json.dumps(json_ld, ensure_ascii=False, separators=(',', ':')),
        'canonical_url': request.build_absolute_uri('/'),
        'og_image': request.build_absolute_uri('/static/img/lorvessa-emblem.webp'),
        'lcp_image': lcp_image,
    }
    response = render(request, 'pages/home.html', context)
    response['Cache-Control'] = 'private, no-store'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


@require_POST
def add_comment(request):
    """Ziyaretçi yorumu ekler; ardından yorum bölümüne döner."""
    last = request.session.get('last_comment_ts')
    try:
        last_ts = float(last) if last is not None else 0
    except (TypeError, ValueError):
        last_ts = 0
    if last_ts and (time.time() - last_ts) < 45:
        messages.error(request, 'Lütfen yeni yorum için kısa bir süre bekleyin.')
        return redirect(reverse('home') + '#yorumlar')

    form = SiteCommentForm(request.POST)
    if form.is_valid():
        SiteComment.objects.create(
            author_name=form.cleaned_data['author_name'],
            body=form.cleaned_data['body'],
        )
        request.session['last_comment_ts'] = time.time()
        messages.success(request, 'Yorumunuz yayınlandı. Teşekkür ederiz.')
        return redirect(reverse('home') + '#yorumlar')

    messages.error(request, 'Yorum gönderilemedi. Ad ve yorum alanlarını kontrol edin.')
    return redirect(reverse('home') + '#yorumlar')


def robots_txt(request):
    site = request.build_absolute_uri('/').rstrip('/')
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /media/private/',
        '',
        '# AI / LLM crawlers',
        'User-agent: GPTBot',
        'Allow: /',
        '',
        'User-agent: ChatGPT-User',
        'Allow: /',
        '',
        'User-agent: Google-Extended',
        'Allow: /',
        '',
        'User-agent: anthropic-ai',
        'Allow: /',
        '',
        'User-agent: Claude-Web',
        'Allow: /',
        '',
        'User-agent: PerplexityBot',
        'Allow: /',
        '',
        'User-agent: Bytespider',
        'Allow: /',
        '',
        f'Sitemap: {site}/sitemap.xml',
        f'LLMs: {site}/llms.txt',
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


def llms_txt(request):
    """AI asistanlarının siteyi doğru özetlemesi için llms.txt."""
    contact = ContactInfo.objects.filter(is_active=True).first()
    services = ServiceItem.objects.filter(is_active=True)
    about = AboutSection.objects.filter(is_active=True).first()
    site = request.build_absolute_uri('/').rstrip('/')
    phone = contact.phone if contact and contact.phone else '+90 506 679 17 21'
    address = (
        contact.address
        if contact and contact.address
        else 'Huzurevleri, 14. Sk. 22-15, 21070 Kayapınar/Diyarbakır'
    )

    lines = [
        '# Lorvessa Mobilya',
        '',
        '> Diyarbakır Kayapınar merkezli özel ölçü mobilya üreticisi. '
        'Mutfak, dolap, ofis mobilyası, ahşap uygulama, CNC ve montaj.',
        '',
        f'- Site: {site}',
        f'- Telefon: {phone}',
        f'- Adres: {address}',
        '- Slogan: Tasarım · Konfor · Kalite',
        '- Bölge: Diyarbakır, Kayapınar, Türkiye',
        '',
        '## Hizmetler',
        '',
    ]
    for s in services:
        lines.append(f'- {s.title}: {s.description}')
    lines.extend([
        '',
        '## Hakkında',
        '',
    ])
    if about and about.content:
        lines.append(about.content.strip())
    else:
        lines.append(
            'Lorvessa Mobilya; kişiye özel mobilya üretimi, dayanıklı malzeme ve '
            'usta işçilikle yaşam alanları tasarlar.'
        )
    lines.extend([
        '',
        '## Sayfa bölümleri',
        '',
        f'- Ana sayfa: {site}/#anasayfa',
        f'- Hakkımızda: {site}/#hakkimizda',
        f'- Hizmetler: {site}/#hizmetler',
        f'- Galeri: {site}/#galeri',
        f'- İletişim: {site}/#iletisim',
        '',
        '## Özet (AI için)',
        '',
        'Lorvessa Mobilya, Diyarbakır’da özel ölçü mobilya ve ahşap iç mekân '
        'çözümleri sunan bir mobilya atölyesi / mağazasıdır. Müşteriler mutfak '
        'dolabı, gardırop, vestiyer, ticari alan mobilyası, kapı, restorasyon, '
        'CNC kesim ve montaj için Lorvessa ile iletişime geçebilir.',
        '',
    ])
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


sitemaps = {
    'static': StaticViewSitemap,
}


def sitemap_xml(request):
    return sitemap(request, sitemaps)
