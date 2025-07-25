from django.shortcuts import render, get_object_or_404
from .models import LandingPage

def landing_detail(request, slug):
    landing = get_object_or_404(LandingPage, slug=slug)
    hero_block = getattr(landing, 'hero_block', None)
    benefits_block = getattr(landing, 'benefits_block', None)
    solutions_block = getattr(landing, 'solutions_block', None)
    tariff_block = getattr(landing, 'tariff_block', None)
    cases_block = getattr(landing, 'cases_block', None)
    certificate_block = getattr(landing, 'certificate_block', None)
    clients_block = getattr(landing, 'clients_block', None)
    faq_block = getattr(landing, 'faq_block', None)
    about_block = landing.about_block.filter(active=True).first()

    block_map = [
        ('hero_block', 'Главная'),
        ('tariff_block', 'Тарифы'),
        ('cases_block', 'Кейсы'),
        ('faq_block', 'FAQ'),
    ]
    nav_items = []
    for attr, nav_title in block_map:
        block = getattr(landing, attr, None)
        if block and getattr(block, 'active', True) and getattr(block, 'slug', None):
            nav_items.append({
                'slug': block.slug,
                'title': nav_title,  # всегда из block_map!
            })

    return render(request, 'landings/landing_detail.html', {
        'landing': landing,
        'hero_block': hero_block,
        'benefits_block': benefits_block,
        'solutions_block': solutions_block,
        'tariff_block': tariff_block,
        'cases_block': cases_block,
        'certificate_block': certificate_block,
        'clients_block': clients_block,
        'faq_block': faq_block,
        'about_block': about_block,
        'nav_items': nav_items,
    })

def main_landing(request):
    landing = get_object_or_404(LandingPage, is_main=True)
    return landing_detail(request, landing.slug)