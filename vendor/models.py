from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

# Create your models here.
class address(models.Model):
    line1 = models.CharField(max_length=155)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    pincode_regex = RegexValidator(regex=r'^\+?1?\d{6}$')
    pincode = models.CharField(validators=[pincode_regex], max_length=6)

    def __str__(self):
        return self.line1

class vendor(models.Model):
    choices = (
        ("1", "Pending"),
        ("2", "Approved"),
        ("3", "Rejected"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = PhoneField(help_text='Contact phone number')
    aadhar_regex = RegexValidator(regex=r'^\+?1?\d{12}$', message="Aadhar number must be entered only 12 digits allowed.")
    aadhar_number = models.CharField(validators=[aadhar_regex], max_length=12)
    address = models.ForeignKey(address, on_delete=models.SET_NULL, null=True, blank=True)
    aadhar_front = models.FileField(null=True, blank=True, upload_to="aadhar")
    aadhar_back = models.FileField(null=True, blank=True,upload_to="aadhar")
    created_date = models.DateTimeField(default=now, blank=True)
    status = models.CharField(choices=choices,max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def __init__(self, *args, **kwargs):
        super(vendor, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status != self.__original_status:
            if self.status == "2":
                msg = "Approved"
            elif self.status == "3":
                msg = "Rejected"
            elif self.status == "1":
                msg = "Pending"
            send_mail('HOPON - Account verified!',"Your request for Vendor with HopON is "+ msg +"\n \nPlease login to your account and proceed further.", settings.EMAIL_HOST_USER, [self.user.email])


        super(vendor, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

class company(models.Model):
    choices = (
        ("1", "Pending"),
        ("2", "Aproved"),
        ("3", "Rejected"),
    )
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=255)
    cars = models.IntegerField(null=True)
    address = models.ForeignKey(address, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(default=now, blank=True)
    site_docFront = models.FileField(null=True, blank=True, upload_to="Site Document")
    site_docBack = models.FileField(null=True, blank=True, upload_to="Site Document")
    status = models.CharField(choices=choices,max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(company, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status != self.__original_status:
            if self.status == "2":
                msg = "Approved"
            elif self.status == "3":
                msg = "Rejected"
            elif self.status == "1":
                msg = "Pending"
            send_mail('HOPON - Site Registration verified!',"Your request for Vendor with HopON is "+ msg +"\n \nPlease login to your account and add cars.", settings.EMAIL_HOST_USER, [self.vendor.user.email])


        super(company, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

class otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    datetime = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.email
    
    


