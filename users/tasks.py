
from django.core.mail import send_mail
from goodreads.celery import app

@app.task()
def send_email_task(subject,message,recipient_list):
     send_mail(subject,
                      message,
                      'raxmatjonhamidov242@gmail.com',
                     recipient_list
                      )