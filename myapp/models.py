from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Consumer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Student Name")
    email = models.EmailField(max_length=277, verbose_name="Student Email")
    image = models.ImageField(upload_to='consumer_images/', null=True, blank=True, verbose_name="Consumer Image")
    content = models.TextField(verbose_name="Consumer Content", blank=True, null=True)

    def __str__(self):
        return str(self.id)

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

models.signals.post_save.connect(create_profile, sender=User)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    card_holder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_name = models.CharField(max_length=100)
    merchant_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    is_fraudulent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.card_holder_name} - {self.transaction_amount}"


