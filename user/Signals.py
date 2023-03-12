
# code
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Like
from notifications.signals import notify
# from myapp.utils import send_notification

# def notify_user(sender, instance, **kwargs):
# #    send_notification(instance.ordered_by)
#     print('iamnotify')

# post_save.connect(notify_user, sender=Like)

# @receiver(post_save, sender=Like)
# def notify_like(sender,instance, **kwargs):
#     print('i ama a notify',sender)

@receiver(sender=Like)
def user_signed_in(request, uid, **kwargs):    
  notify.send(uid, recipient=uid, verb=("You signed in"))