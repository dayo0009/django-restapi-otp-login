from django.conf import settings
from django.db import models
from ..managers import CustomUserManager


class LoginOtp(models.Model):
    DoesNotExist = None

    id = models.BigAutoField(primary_key=True)
    login = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_login_id', blank=True, null=True,
                              on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, max_length=1)
    otp = models.CharField(max_length=6, null=True, blank=True, unique=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    otp_max_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "login_otp"
        app_label = "home"

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        return instance

