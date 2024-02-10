from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

user = get_user_model()


# Create your models here.
class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(user, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.user}: {self.token}")

    class Meta:
        unique_together = ("token", "user")
