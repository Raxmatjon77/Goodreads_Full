from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    profile_picture=models.ImageField(default='default_profile_pic.jpg')
<<<<<<< HEAD
    

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_sent')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"from {self.sender} to {self.receiver}   status :{self.status}"
=======
    created_at=models.DateTimeField(default=timezone.now)
    
    from django.db import models

# Create your models here.


class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friendships')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friendships')
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    
    
    def __str__(self) -> str:
        return f" from {self.from_user.username} to {self.to_user.username} status : {self.status}"
>>>>>>> 02cfc3e1c6c477527cbc08d4de2731a54e1189ed
