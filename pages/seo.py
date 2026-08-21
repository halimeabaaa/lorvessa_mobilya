"""SEO / site bilgisi yardımcıları."""
from django.conf import settings


def absolute_url(path=''):
    base = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000').rstrip('/')
    if not path:
        return base
    if path.startswith('http'):
        return path
    return f"{base}/{path.lstrip('/')}"


def default_seo():
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'Lorvessa Mobilya'),
        'site_url': absolute_url(),
        'seo_title': (
            'Lorvessa Mobilya | Özel Ölçü Mobilya, Mutfak ve Dolap Yapımı Diyarbakır'
        ),
        'seo_description': (
            'Lorvessa Mobilya — Diyarbakır Kayapınar’da özel ölçü mobilya üretimi, '
            'mutfak dolabı, gardırop, vestiyer, ofis mobilyası, ahşap uygulama, '
            'CNC kesim, restorasyon ve montaj hizmetleri. Tasarım, konfor, kalite.'
        ),
        'seo_keywords': (
            'Lorvessa Mobilya, Diyarbakır mobilya, Kayapınar mobilya, özel ölçü mobilya, '
            'mutfak dolabı Diyarbakır, gardırop yapımı, vestiyer, TV ünitesi, '
            'ofis mobilyası, ahşap panel, CNC kesim, mobilya restorasyon, '
            'kişiye özel mobilya, lake mobilya'
        ),
        'seo_locale': 'tr_TR',
        'seo_geo_region': 'TR-21',
        'seo_geo_placename': 'Diyarbakır',
    }


def build_json_ld(contact=None, services=None, about=None, request=None):
    """LocalBusiness + WebSite + FAQ structured data."""
    site_url = absolute_url()
    if request is not None:
        site_url = request.build_absolute_uri('/').rstrip('/')

    logo = f'{site_url}/static/img/lorvessa-emblem.png'
    if contact and hasattr(contact, 'phone_e164'):
        phone = f'+{contact.phone_e164()}'
    else:
        phone = (contact.phone if contact and contact.phone else '+905066791721')
    address = (
        contact.address
        if contact and contact.address
        else 'Huzurevleri, 14. Sk. 22-15, 21070 Kayapınar/Diyarbakır'
    )
    email = contact.email if contact and contact.email else None

    description = default_seo()['seo_description']
    if about and about.content:
        description = ' '.join(about.content.split())[:300]

    business = {
        '@type': ['FurnitureStore', 'HomeAndConstructionBusiness', 'LocalBusiness'],
        '@id': f'{site_url}/#business',
        'name': 'Lorvessa Mobilya',
        'alternateName': ['Lorvessa', 'Lorvessa Mobilya Diyarbakır'],
        'url': site_url,
        'logo': logo,
        'image': logo,
        'description': description,
        'telephone': phone,
        'priceRange': '$$',
        'currenciesAccepted': 'TRY',
        'paymentAccepted': 'Cash, Credit Card',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': address,
            'addressLocality': 'Kayapınar',
            'addressRegion': 'Diyarbakır',
            'postalCode': '21070',
            'addressCountry': 'TR',
        },
        'geo': {
            '@type': 'GeoCoordinates',
            'latitude': 37.936652,
            'longitude': 40.193795,
        },
        'areaServed': [
            {'@type': 'City', 'name': 'Diyarbakır'},
            {'@type': 'AdministrativeArea', 'name': 'Kayapınar'},
            {'@type': 'Country', 'name': 'Türkiye'},
        ],
        'knowsLanguage': ['tr'],
        'slogan': 'Tasarım · Konfor · Kalite',
        'sameAs': [],
    }
    if email:
        business['email'] = email

    if services:
        business['hasOfferCatalog'] = {
            '@type': 'OfferCatalog',
            'name': 'Lorvessa Mobilya Hizmetleri',
            'itemListElement': [
                {
                    '@type': 'Offer',
                    'itemOffered': {
                        '@type': 'Service',
                        'name': s.title,
                        'description': s.description,
                        'provider': {'@id': f'{site_url}/#business'},
                        'areaServed': 'Diyarbakır',
                    },
                }
                for s in services
            ],
        }

    website = {
        '@type': 'WebSite',
        '@id': f'{site_url}/#website',
        'url': site_url,
        'name': 'Lorvessa Mobilya',
        'description': default_seo()['seo_description'],
        'inLanguage': 'tr-TR',
        'publisher': {'@id': f'{site_url}/#business'},
    }

    webpage = {
        '@type': 'WebPage',
        '@id': f'{site_url}/#webpage',
        'url': site_url,
        'name': default_seo()['seo_title'],
        'isPartOf': {'@id': f'{site_url}/#website'},
        'about': {'@id': f'{site_url}/#business'},
        'description': default_seo()['seo_description'],
        'inLanguage': 'tr-TR',
        'primaryImageOfPage': logo,
    }

    faq = {
        '@type': 'FAQPage',
        '@id': f'{site_url}/#faq',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': 'Lorvessa Mobilya nerede hizmet veriyor?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        'Lorvessa Mobilya Diyarbakır Kayapınar’da (Huzurevleri, 14. Sk. 22-15) '
                        'özel ölçü mobilya üretimi, montaj ve ahşap uygulama hizmetleri sunar.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': 'Özel ölçü mobilya yaptırabilir miyim?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        'Evet. Lorvessa; mutfak, banyo, gardırop, vestiyer, TV ünitesi ve diğer '
                        'dolap sistemlerinde kişiye özel ölçü ve tasarımla üretim yapar.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': 'Lorvessa Mobilya hangi hizmetleri sunuyor?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        'Özel ölçü mobilya üretimi, dolap yapımı, iç mekân ahşap uygulamaları, '
                        'ofis ve ticari alan mobilyaları, kapı ve doğrama, restorasyon, montaj, '
                        'ahşap merdiven, CNC kesim ve projelendirme/tasarım hizmetleri sunulur.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': 'Lorvessa Mobilya iletişim numarası nedir?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': f'Lorvessa Mobilya telefon: {phone}. Adres: {address}.',
                },
            },
            {
                '@type': 'Question',
                'name': 'Keşif, ölçülendirme ve teklif süreci nasıl ilerliyor?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        'Telefon veya WhatsApp görüşmesinin ardından ihtiyaç belirlenir, '
                        'uygun olduğunda yerinde ölçü alınır ve malzeme, tasarım, üretim '
                        'ile montaj kapsamını içeren teklif hazırlanır.'
                    ),
                },
            },
        ],
    }

    return {
        '@context': 'https://schema.org',
        '@graph': [business, website, webpage, faq],
    }
