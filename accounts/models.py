from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.validators import RegexValidator
from django.shortcuts import reverse


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, firstname, middlename, lastname, email, password, **extra_fields):
        values = [email, firstname, middlename, lastname, username]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, firstname, middlename, lastname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, firstname, middlename, lastname, email, password, **extra_fields)

    def create_superuser(self, username, firstname, middlename, lastname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, firstname, middlename, lastname, email, password, **extra_fields)


class Region(models.Model):
    postcode = models.IntegerField()
    name = models.CharField(max_length=70, blank=False, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    postcode = models.IntegerField()
    name = models.CharField(max_length=70, blank=False, null=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(models.Model):
    postcode = models.IntegerField()
    name = models.CharField(max_length=70, blank=False, null=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female')]

    Roles = [(1, 'Admin'), (2, 'Accountant'), (3, 'Store'), (4, 'Surveyor')]
    APPROVAL_CHOICES = (
        ('n', 'Not Requested For Approval'),
        ('p', 'Approval Application on Pending'),
        ('d', 'Approval Request Declined'),
        ('a', 'Verified')
    )

    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(unique=True, verbose_name=('email address'))
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=150, blank=True, null=True)
    lastname = models.CharField(max_length=50)
    """ is_superuser = models.BooleanField('Superuser status', default=False, help_text='Designates whether the user can log into '
                                                                            'this admin site.',) """
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated '
                                                                      'as active. Unselect this instead of deleting '
                                                                      'accounts.',)
    is_staff = models.BooleanField('staff status', default=False, help_text='Designates whether the user can log into '
                                                                            'this admin site.',)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    last_login = models.DateTimeField(null=True)
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    mobile = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    region = models.ForeignKey(
        'Region', on_delete=models.CASCADE, related_name='User_Region', blank=True, null=True)
    district = models.ForeignKey(
        'District', related_name='User_District', on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to="photo/", blank=True, null=True)
    user_roles = models.IntegerField(default=4, choices=Roles)
    approval_status = models.CharField(
        max_length=2, choices=APPROVAL_CHOICES, default=APPROVAL_CHOICES[0][0],)
    Bio = models.TextField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'middlename',
                       'lastname', 'mobile', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.pk})

    def get_full_name(self):
        fullname = '%s %s %s' % (
            self.firstname, self.middlename, self.lastname)
        return fullname.strip()

    def get_short_name(self):
        return self.firstname

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
