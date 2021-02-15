from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


class SurveyProject(models.Model):
    proid = models.AutoField(primary_key=True)
    author = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Creator')
    site_No = models.IntegerField(blank=False, null=True)
    Region = models.ForeignKey(
        'accounts.Region', on_delete=models.CASCADE, related_name='Source_Region')
    District = models.ForeignKey(
        'accounts.District', on_delete=models.CASCADE, related_name='Source_District')
    Ward = models.ForeignKey(
        'accounts.Ward', on_delete=models.CASCADE, related_name='Source_Ward')
    Location = models.CharField(max_length=55, blank=True)
    Current_source = models.CharField(max_length=100, blank=True)
    Distance_source = models.CharField(max_length=20, blank=True)
    Affected_people = models.IntegerField(blank=True)
    Picture = models.ImageField(
        upload_to="photo/currSource/", blank=True, null=True)
    Video = models.FileField(
        upload_to="video/currSource/", blank=True, null=True)
    Attachment = models.FileField(
        upload_to="attachments/currSource/", blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)


def __str__(self):
    return self.site_no


class Store(models.Model):
    item = models.ForeignKey(
        'Equipment', on_delete=models.CASCADE, related_name='Stored_items')
    amount = models.IntegerField()
    buy_time = models.DateTimeField(default=timezone.now)
    uploader = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Uploaded_by')

def __str__(self):
    return self.item.name

class Equipment(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    size = models.IntegerField()
    unit_of_size = models.CharField(max_length=20, blank=False, null=False)
    material = models.CharField(max_length=20, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(
        upload_to="photo/equipments/", blank=True, null=True)

    def __str__(self):
        return self.name


class WellInfo(models.Model):
    site = models.OneToOneField(
        SurveyProject, on_delete=models.CASCADE, related_name='WellSite_Info')
    contact1 = models.CharField(max_length=20, blank=True)
    contact2 = models.CharField(max_length=20, blank=True, null=True)
    depth = models.IntegerField()
    picture = models.ImageField(
        upload_to="photo/well/", blank=True, null=True)
    Video = models.FileField(
        upload_to="video/well/", blank=True, null=True)
    equipment = models.ManyToManyField(
        Equipment, blank=True, related_name='requirement')


def __str__(self):
    return self.site
