from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Queries(models.Model):
    search = models.CharField(max_length=120, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.search
