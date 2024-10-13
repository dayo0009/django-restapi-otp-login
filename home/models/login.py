from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db import *
from ..managers import CustomUserManager


class Login(AbstractBaseUser):
    DoesNotExist = None
    password = None
    last_login = None
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    verification_code = models.CharField(max_length=8)
    approved = models.CharField(max_length=2)
    date_registered = models.DateTimeField(auto_now_add=True)

    """ enable 2fa for each user in the future with models.BooleanField(default=False) """

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    class Meta:
        db_table = "user_login"
        app_label = "home"

    def __str__(self):
        return str(self.email)

    @staticmethod
    def check_if_email_exists(self):
        email_exists = Login.objects.filter(email=self.email).exists()
        if email_exists is not None:
            return True
        return False

    @staticmethod
    def get_user_by_email(email):
        user_email = Login.objects.get(email=email)
        try:
            user_email
        except DatabaseError:
            return DatabaseError("Error verifying email, check your connection")

    @staticmethod
    def check_if_phone_number_exists(self):
        check_phone = Login.objects.filter(phone_number=self.phone_number).exists()
        if check_phone:
            return True
        return False

    @staticmethod
    def get_user_phone(phone):
        phone = Login.objects.get(phone_number=phone)
        try:
            phone
        except DataError:
            raise DataError
