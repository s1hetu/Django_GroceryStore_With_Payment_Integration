from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

from constants import GENDER_CHOICES


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Female')
    mobile_no = PhoneNumberField(null=True, unique=True)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.image.path)


class Brand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.brand
from django.db import models

# Create your models here.
