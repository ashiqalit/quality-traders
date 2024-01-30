from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
CHOICES = [('1', 'SMS'), ('2', 'Whatsapp'),]
class Profile(models.Model):
    # user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    username = models.CharField(max_length=100,null=False,blank=False,unique=True)
    phone=models.CharField(max_length=15,null=False,blank=False)
    otp=models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=False,blank=False,default='ashiqalit@gmail.com')
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)

    def __str__(self):
        return self.username 