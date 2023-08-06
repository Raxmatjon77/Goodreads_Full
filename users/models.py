from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    profile_picture=models.ImageField(default='default_profile_pic.jpg')

    




class Friendship(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friendships')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friendships')
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    
    
    def __str__(self) -> str:
        return f" from {self.sender.username} to {self.receiver.username} status : {self.status}"

