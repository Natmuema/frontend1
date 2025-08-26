from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ("investor", "Investor"),
        ("artist", "Artist"),
        ("other", "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=32, choices=USER_TYPE_CHOICES, default="other")

    def __str__(self):
        return f"Profile<{self.user.username}:{self.user_type}>"

# Create your models here.
