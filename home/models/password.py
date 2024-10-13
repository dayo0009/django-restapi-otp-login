from django.db import models
from django.conf import settings
from ..managers import CustomUserManager


class Password(models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='login_id', blank=True, null=True,
                              on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "confirm_pass"
        app_label = "home"

    def register(self):
        self.save()
