import nested_admin
from django.contrib import admin
from .models import LandingPage, HeroBlock, BenefitsBlock, SolutionsBlock, TariffBlock, TariffCard, TariffProperty, AboutBlock, CasesBlock, CasesBlockItem, CertificateBlock, CertificateBlockItem, ClientsBlock, FaqBlock, FaqBlockItem

class HeroBlockInline(nested_admin.NestedStackedInline):
    model = HeroBlock
    extra = 1
    max_num = 1

class BenefitsBlockInline(nested_admin.NestedStackedInline):
    model = BenefitsBlock
    can_delete = False
    max_num = 1

class SolutionsBlockInline(nested_admin.NestedStackedInline):
    model = SolutionsBlock
    can_delete = False
    max_num = 1

class TariffPropertyInline(nested_admin.NestedTabularInline):
    model = TariffProperty
    extra = 1

class TariffCardInline(nested_admin.NestedStackedInline):
    model = TariffCard
    extra = 1
    inlines = [TariffPropertyInline]

class TariffBlockInline(nested_admin.NestedStackedInline):
    model = TariffBlock
    inlines = [TariffCardInline]
    extra = 1
    max_num = 1
    can_delete = False

class AboutBlockInline(nested_admin.NestedStackedInline):
    model = AboutBlock
    can_delete = False
    max_num = 1

class CasesBlockItemsInline(nested_admin.NestedStackedInline):
    model = CasesBlockItem
    extra = 1

class CasesBlockInline(nested_admin.NestedStackedInline):
    model = CasesBlock
    inlines = [CasesBlockItemsInline]
    can_delete = False
    max_num = 1

class CertificateBlockItemsInline(nested_admin.NestedStackedInline):
    model = CertificateBlockItem
    extra = 1

class CertificateBlockInline(nested_admin.NestedStackedInline):
    model = CertificateBlock
    inlines = [CertificateBlockItemsInline]
    can_delete = False
    max_num = 1

class ClientsBlockInline(nested_admin.NestedStackedInline):
    model = ClientsBlock
    extra = 1

class FaqBlockItemsInline(nested_admin.NestedStackedInline):
    model = FaqBlockItem
    extra = 1

class FaqBlockInline(nested_admin.NestedStackedInline):
    model = FaqBlock
    inlines = [FaqBlockItemsInline]
    can_delete = False
    max_num = 1

class LandingPageAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'is_main')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        HeroBlockInline,
        BenefitsBlockInline,
        SolutionsBlockInline,
        TariffBlockInline,
        AboutBlockInline,
        CasesBlockInline,
        CertificateBlockInline,
        ClientsBlockInline,
        FaqBlockInline,
    ]

    def save_model(self, request, obj, form, change):
        if obj.is_main:
            # Сбросить is_main у всех остальных лендингов
            LandingPage.objects.exclude(pk=obj.pk).update(is_main=False)
        super().save_model(request, obj, form, change)

@admin.register(BenefitsBlock)
class BenefitsBlockAdmin(admin.ModelAdmin):
    list_display = ('landing', 'text1', 'text2', 'text3')

@admin.register(HeroBlock)
class HeroBlockAdmin(admin.ModelAdmin):
    list_display = ('landing', 'title')

@admin.register(SolutionsBlock)
class SolutionsBlockAdmin(admin.ModelAdmin):
    list_display = ('landing', 'title')

@admin.register(TariffBlock)
class TariffBlockAdmin(admin.ModelAdmin):
    inlines = [TariffCardInline]

@admin.register(TariffCard)
class TariffCardAdmin(admin.ModelAdmin):
    inlines = [TariffPropertyInline]

@admin.register(AboutBlock)
class AboutBlockAdmin(admin.ModelAdmin):
    list_display = ('landing', 'title')

admin.site.register(LandingPage, LandingPageAdmin)
