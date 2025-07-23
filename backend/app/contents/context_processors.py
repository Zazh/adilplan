# contents/context_processors.py

from .models import Contact, Address, Email, Phones

def contacts(request):
    contact = Contact.objects.first()  # или фильтрация по сайту, если нужно
    address = Address.objects.filter(contact=contact)
    email = Email.objects.filter(contact=contact)
    phones = Phones.objects.filter(contact=contact)
    return {
        'contact': contact,
        'address': address,
        'email': email,
        'phones': phones,
    }
