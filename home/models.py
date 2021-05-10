from PIL import Image
from django.db import models
from django.contrib.auth.models import User

from win32api import GetSystemMetrics

from django.conf import settings

# Create your models here.
import uuid
class Domain(models.Model):
    domain=models.CharField(max_length=20)
    def __str__(self):
        return self.domain



def get_default_profile_image():
    return "proforma/proforma.png"

class Administrator(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL , related_name="artical" , on_delete=models.CASCADE)
    id=models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    title = models.CharField(max_length=100)

    First_name = models.CharField(max_length=30, blank=True)
    Last_name = models.CharField(max_length=30, blank=True)

    proforma_image = models.ImageField(upload_to='proforma/', null=True, blank=True,
                                       default=get_default_profile_image, )

    bio = models.TextField(blank=True)

    domain=models.ManyToManyField(Domain , related_name='field')


    def __str__(self):
        return self.title

    def save(self):
        if not self.proforma_image:
            return

        super(Administrator, self).save()
        image = Image.open(self.proforma_image)
        (width, height) = image.size
        print(width , height)
        size = (GetSystemMetrics(0),  GetSystemMetrics(1))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.proforma_image.path)



