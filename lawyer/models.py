from django.db import models

# Create your models here.


from django.db import models

from users.models import User


class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firm = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.user} {self.user} - {self.firm}"