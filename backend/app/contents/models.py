from django.db import models

class Contact(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='Contact us', default='Contact us')
    name = models.CharField(max_length=255, blank=True, verbose_name='Legal company name', default='ТОО abplan.kz')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Company legal name: {self.name}, title: {self.title}'

class Phones(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField(max_length=255, verbose_name='phone', default='+7')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Phone: {self.phone}'

class Email(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='email')
    email = models.EmailField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Email: {self.email}'


class Address(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='address')
    address = models.CharField()
    map = models.CharField(max_length=255, blank=True, default='put the link here')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Email: {self.address}'

class Social(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='social')
    svg_path = models.TextField(blank=True)
    name = models.CharField(blank=True)
    link = models.CharField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.link}'
