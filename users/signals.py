from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser
from django.core.mail import send_mail
@receiver(post_save,sender=CustomUser)

def send_welcome_email(sender,instance,created,**kwargs):
    
    if created:
        send_mail('Welcome to Goodreads Clone',
                      f"Hi {instance.username} , Welcome to Goodreads . Enjoy books and reviews(Assalomu Alaykum, {instance.username} , Bizning Goodreads kutubxonamizga xush kelibsiz,Kitoblardan va unga qoldirirlgan izoxlardan rohatlaning ! (Raxmatjon Hamidov) )",
                      'raxmatjonhamidov242@gmail.com',
                      [instance.email]
                      )
    
    print('signal handleer called')