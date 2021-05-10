import os

from django.conf import settings
from django.db import models
from win32api import GetSystemMetrics

from account.models import Account

from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from PIL import Image

from usrprofile.MultiWidget import MyTestField
import  time

def get_default_profile_image():
    return "default_proforma/proforma.png"

class MyProfile(models.Model):
    AVAILABLE=(
        ('For hire' , 'hire'),
        ('Professional' , 'Professional'),
        ('student' , 'Student')
    )

    user=models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name='profile')
    First_name=models.CharField(max_length=30 , blank=True)
    Last_name=models.CharField(max_length=30 , blank=True)

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    contact=models.BigIntegerField( blank=True)

    proforma_image=models.ImageField(upload_to='proforma/', null=True , blank=True , default=get_default_profile_image ,)

    DOB=models.DateField(null=True , blank=True)
    bio = models.TextField(blank=True)

    special_activity=models.TextField(blank=True , max_length=500)

    specialist=models.CharField(max_length=100 , blank=True)

    available=models.CharField(max_length=30 , choices=AVAILABLE , default='For hire')

    experience=models.IntegerField( default=0 )



    # def delete(self, *args, **kwargs):
    #     if os.path.isfile(self.proforma_image.path):
    #         os.remove(self.proforma_image.path)
        # super(MyProfile, self).delete(*args, **kwargs)


    def save(self , *args , **kwargs):
        if not self.proforma_image:
            return super(MyProfile, self).save( *args , **kwargs)

        super(MyProfile, self).save( *args , **kwargs)

        image = Image.open(self.proforma_image)
        (width, height) = image.size
        print(width , height)
        size = (GetSystemMetrics(0),  GetSystemMetrics(1))
        print(size , '-------------')
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.proforma_image.path)
        image.close()

        # super(MyProfile, self).save(*args, **kwargs)



    def __str__(self):
        return "{} {}".format(self.user.username , self.First_name)


class Hobbies(models.Model):
    myprofile=models.ForeignKey(MyProfile , on_delete=models.CASCADE, related_name='user_hobbies')
    Name=models.CharField(max_length=30 , )
    Follow=models.CharField(max_length=50 , )

    def __str__(self):
        return self.myprofile.user.username



@receiver(post_save , sender=Account)
def create_user_profile(sender , instance , created , **kwargs):
    first_name = getattr(instance, 'first_name', None)
    last_name = getattr(instance, 'last_name', None)
    contact = getattr(instance, 'contact', None)
    print(first_name , last_name , contact)
    if created:
        print("profile object is created")
        MyProfile.objects.create(First_name=first_name, Last_name=last_name , contact=contact ,  user=instance ,email=instance.email)
    else:
        print('profile are updated')


# @receiver(post_save , sender=MyProfile)
# def create_user_hobbies(sender , instance , created , **kwargs):
#     if created:
#         print('hobbies are created')
#         # Hobbies.objects.create(myprofile=instance)
#     else:
#         print('hobbies are updated')



def get_edu_document_filepath(self, filename):
    filename, file_extension = os.path.splitext(filename)
    print(file_extension,'----------------------')

    return "education/{}/{}{}".format(self.profile.user.username,self.board_class , file_extension)



class MyEdu(models.Model):
    profile=models.ForeignKey(MyProfile , on_delete=models.CASCADE , related_name='my_edu' , blank=True)
    board_class=models.CharField(max_length=30 , blank=True )
    board_name=models.CharField(max_length=30 , blank=True)
    year=models.IntegerField(blank=True)
    percentage=models.CharField(max_length=30)
    file=models.ImageField(upload_to=get_edu_document_filepath , default='none')

    def __str__(self):
        return 'user {} education'.format(self.profile.First_name)

    def save(self, *args, **kwargs):

            print(self.file , 'ijdfig====')
            # print("hgdsf--------")
            # file_path = 'media/education/{}/{}.png'.format(self.profile.user.username,self.board_class)
            # print(self.file)
            # image = Image.open(self.file)
            # image.save(file_path)
            super(MyEdu, self).save(*args, **kwargs)
@receiver(pre_delete , sender=MyEdu)
def pre_delete_document(sender , instance ,**kwargs):
    try:
     instance.file.delete()
    except PermissionError:
     pass

# @receiver(post_save , sender=MyEdu)
# def create_user_education(sender , instance , created , **kwargs):
#     if created:
#         print('hobbies are created')
#
#     else:
#         file_type = getattr(instance, 'file_type', None)
#         instance.file.delete()
#         # instance.file=file_type
#         with open('media_cdn/' + file_type.name, 'wb+') as destination:
#             for chunk in file_type.chunks():
#                 destination.write(chunk)
#         print(instance.file)
#         print('hobbies are updated')


class MySkills(models.Model):
    profile=models.ForeignKey(MyProfile , on_delete=models.CASCADE , related_name='myskills')
    session=models.CharField(max_length=30 , blank=True)
    skill_name=models.CharField(max_length=150 , blank=True ,)
    skill_dependency=models.CharField(max_length=250 , blank=True)
    skill_text=models.TextField(blank=True)

    def __str__(self):
        return '{} skill is {}'.format(self.profile.user , self.skill_name)




def get_exp_document_filepath(self, filename):
    filename, file_extension = os.path.splitext(filename)
    print(file_extension,'----------------------')

    return "expreience/{}/{}{}".format(self.profile.user.username, self.job_title, file_extension)

class MyExpreience(models.Model):
    profile=models.ForeignKey(MyProfile , on_delete=models.CASCADE , related_name='my_exp' , blank=True)
    expreience=models.CharField(max_length=30 , blank=True)
    job_title=models.CharField(max_length=30 , blank=True)
    company_name=models.CharField(max_length=30 ,)
    file=models.ImageField(upload_to=get_exp_document_filepath , default='none')

    def __str__(self):
        return 'user {} Expreience'.format(self.profile.First_name)



@receiver(pre_delete , sender=MyExpreience)
def per_delete_document(sender , instance ,**kwargs):
    try:
     instance.file.delete()
    except PermissionError:
      pass


def get_activity_document_filepath(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return "activity/{}/report{}".format(self.activity_name, file_extension)


def get_activity_headimage_filepath(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return "activity/{}/headImg{}".format(self.activity_name, file_extension)

from usrprofile.django_resized import ResizedImageField

class MyActivity(models.Model):
    profile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='my_activity', blank=True)
    activity_name=models.CharField(max_length=50 , blank=True , )
    activity_url=models.URLField(max_length=100 , default='none')
    activity_head_image=ResizedImageField( upload_to='HeadImage/' , default='none')
    activity_head_report=models.FileField(upload_to='Report/' , default='none')

    def save(self):
        super(MyActivity, self).save()
        print(self.activity_head_image)
        if not self.activity_head_image:
            return

        if self.activity_head_image != 'none':
            super(MyActivity, self).save()
            image = Image.open(self.activity_head_image)
            (width, height) = image.size
            print(width, height)
            size = (1080, 1080)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.activity_head_image.path)

        super(MyActivity, self).save()

    def __str__(self):
        return '{} activity is'.format(self.profile.First_name)

# @receiver(pre_save ,sender=MyActivity )
# def per_activity_save_images(sender , instance ,**kwargs):
#     image = Image.open(instance.activity_head_image)
#     (width, height) = image.size
#     size = (1080, 1080)
#     image = image.resize(size, Image.ANTIALIAS)
#     image.save(instance.activity_head_image.path)

# @receiver(pre_delete , sender=MyActivity)
# def per_activity_delete_document(sender , instance ,**kwargs):
#     instance.activity_head_report.delete()
#     instance.activity_head_image.delete()


@receiver(pre_delete , sender=MyActivity)
def per_activity_delete_document(sender , instance ,**kwargs):
    try:
     instance.activity_head_report.delete()
     instance.activity_head_image.delete()
    except PermissionError:
        pass


class Uploda_Resume(models.Model):
    profile = models.OneToOneField(MyProfile, on_delete=models.CASCADE, related_name='my_resume')
    file= models.FileField(upload_to='Resume/', default='none')

class Country(models.Model):
    name = models.CharField(max_length=30 , null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30 , null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE , related_name='city_set')


    def __str__(self):
        return self.name



class MyAddress(models.Model):
    profile=models.OneToOneField(MyProfile , on_delete=models.CASCADE , related_name='my_address')
    email=models.EmailField(max_length=200)
    contact=models.BigIntegerField( blank=True)
    website=models.URLField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True  )
    postal_code=models.IntegerField()


@receiver(post_save , sender=MyProfile)
def create_user_address(sender , instance , created , **kwargs):
    if created:
        print('address object are created')
        MyAddress.objects.create(profile=instance , email=instance.email)
    else:
        print('address are updated')


class Iam(models.Model):
    profile=models.ForeignKey(MyProfile , on_delete=models.CASCADE , related_name='iam')
    iam=models.CharField(max_length=50)

    def __str__(self):
        return '{} is a {}'.format(self.profile.First_name , self.iam)


@receiver(post_save , sender=MyProfile)

def I_AM_A(sender , instance , created , **kwargs):

    if created:
        print("I_A_AM object is created")
        Iam.objects.create(profile=instance)



