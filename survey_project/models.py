from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


class SurveyProject(models.Model):
    proid = models.AutoField(primary_key=True)
    author = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Creator')
    site_No = models.IntegerField()
    Region = models.ForeignKey(
        'accounts.Region', on_delete=models.CASCADE, related_name='Source_Region', blank=True, null=True)
    District = models.ForeignKey(
        'accounts.District', on_delete=models.CASCADE, related_name='Source_District', blank=True, null=True)
    Ward = models.CharField(max_length=55, blank=True, null=True)
    Location = models.CharField(max_length=55, blank=True, null=True)
    Current_source = models.CharField(max_length=100, blank=True, null=True)
    Distance_source = models.CharField(max_length=20, blank=True, null=True)
    Affected_people = models.IntegerField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)


def __str__(self):
    return self.site_no


class Images(models.Model):
    project = models.ForeignKey(SurveyProject, verbose_name=(
        "SurveywithPhoto"), on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to="photo/currSource/", blank=True, null=True)


def get_absolute_image_url(self):
    return os.path.join(settings.MEDIA_URL, self.picture.url)


class Videos(models.Model):
    project = models.ForeignKey(SurveyProject, verbose_name=(
        "SurveywithVideo"), on_delete=models.CASCADE)
    video = models.FileField(
        upload_to="video/currSource/", blank=True, null=True)

    def get_absolute_video_url(self):
        return os.path.join(settings.MEDIA_URL, self.video.url)


class Attachments(models.Model):
    project = models.ForeignKey(SurveyProject, verbose_name=(
        "SurveywithAttachment"), on_delete=models.CASCADE)
    attachment = models.FileField(
        upload_to="attachments/currSource/", blank=True, null=True)

    def get_absolute_attachment_url(self):
        return os.path.join(settings.MEDIA_URL, self.attachment.url)


class Store(models.Model):
    item = models.ForeignKey(
        'Equipment', on_delete=models.CASCADE, related_name='Stored_items')
    amount = models.IntegerField(blank=True, null=True)
    buy_time = models.DateTimeField(default=timezone.now)
    uploader = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Uploaded_by')


def __str__(self):
    return self.item.name


class Equipment(models.Model):
    UNIT_OF_SIZE = [
        ('Km', 'Kilometre'),
        ('Hm', 'Hectometre'),
        ('Dcm', 'Decametre'),
        ('M', 'Metre'),
        ('Dc', 'Decimetre'),
        ('Cm', 'Centimetre'),
        ('Mm', 'Millimetre')
    ]
    name = models.CharField(max_length=40, blank=False, null=False)
    size = models.IntegerField(blank=True, null=True)
    unit_of_size = models.CharField(
        max_length=4, choices=UNIT_OF_SIZE, default=UNIT_OF_SIZE[0][0], blank=True, null=True)
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
