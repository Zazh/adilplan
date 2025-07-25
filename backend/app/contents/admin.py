from django.contrib import admin
from .models import Contact, Email, Phones, Address, Social

class EmailInlines(admin.TabularInline):
    model = Email
    extra = 1

class PhonesInlines(admin.TabularInline):
    model = Phones
    extra = 1

class AddressInlines(admin.TabularInline):
    model = Address
    extra = 1

class SocialInlines(admin.TabularInline):
    model = Social
    extra = 1

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['title', 'name' ]
    inlines = [EmailInlines, PhonesInlines, AddressInlines, SocialInlines]
