from django.db import models

from lawyer.models import Lawyer
from users.models import User

# Create your models here.


class LandBuyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user} {self.user}"