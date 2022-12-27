from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

# Create your models here.

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    num_packages = models.IntegerField()
    status = models.CharField(max_length=25)
    complete = models.BooleanField(default=False)
    image = models.ImageField(upload_to='alert_images/', storage=default_storage, blank=True, null=True)

@receiver(post_delete, sender=Alert)
def delete_image(sender, instance, **kwargs):
    instance.image.delete(save=False)
