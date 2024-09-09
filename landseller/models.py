from django.db import models

from lawyer.models import Lawyer
from users.models import User

# Create your models here.
# from django.db import models


class LandSeller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.user} {self.user} - Seller"