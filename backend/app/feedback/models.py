from django.db import models

class Feedback(models.Model):
    name = models.CharField('Name', max_length=50)
    phone = models.CharField('Phone', max_length=30)
    source = models.CharField("Источник", max_length=100, blank=True, default="")
    created_at = models.DateTimeField('Create at', auto_now_add=True)

    def __str__(self):
        return f'name: {self.name}, phone{self.phone}'