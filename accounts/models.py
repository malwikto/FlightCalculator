from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model, OneToOneField, CASCADE, CharField, TextField, ImageField, DateField
from PIL import Image


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    profile_picture = ImageField(default="default.jpg", upload_to="profile_pics")
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=20)
    dob = DateField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Profile, self).save()

        img = Image.open(self.profile_picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def __str__(self):
        return f'{self.user.username} profile.'