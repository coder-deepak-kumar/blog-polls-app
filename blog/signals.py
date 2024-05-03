from django.db.models.signals import post_save
from django.dispatch import receiver
from threading import Thread
from django.core.mail import send_mail
from .models import Post, User

@receiver(post_save, sender=Post)
def send_email_to_users(sender, instance, created, **kwargs):
    if created:

        subject = 'New Post Notification'
        message = f'A new post "{instance.title}" has been created. Check it out!'
        sender_email = 'example@gmail.com'  
        
        users = User.objects.all()
        
        def send_email(user):
            recipient_email = user.email
            send_mail(subject, message, sender_email, [recipient_email])

        def send_emails_in_threads():
            threads = []
            for user in users:
                thread = Thread(target=send_email, args=(user,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

        send_emails_in_threads()