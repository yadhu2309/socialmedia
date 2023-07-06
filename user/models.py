from django.db import models
from django.contrib.auth.models import AbstractUser
# from notifications.signals import notify
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    verified = models.BooleanField(default=False)
    googleprofile = models.CharField(max_length=200)

class Details(models.Model):
    address = models.TextField()
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    uid = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)

class UserRequest(models.Model):
    uid = models.ForeignKey(User,related_name='request_user',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    company_name = models.CharField(max_length=50)
    email_company = models.CharField(max_length=50,unique=True)
    # contact_no = models.CharField(max_length=10)
    # about = models.CharField(max_length=100)
    # license_id = models.IntegerField()
    company_address = models.TextField()

    # state = models.CharField(max_length=50)
    # country = models.CharField(max_length=50)
    approve = models.BooleanField(default=False)

class Proposal(models.Model):
    image_one = models.FileField(upload_to='images/')
    image_two = models.FileField(upload_to='images/',blank=True)
    image_three = models.FileField(upload_to='images/',blank=True)
    title = models.CharField(max_length=100)
    describe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey(User,related_name='Proposal_user',on_delete=models.CASCADE)


class PostTry(models.Model):
    image = models.FileField(upload_to='images/')

class ProfileImage(models.Model):
    dp = models.FileField(upload_to='profileImages/')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    uid = models.ForeignKey(User,related_name='user_image',on_delete=models.CASCADE)
    

class follow(models.Model):
    f_uid = models.ForeignKey(User, related_name='fuser', on_delete=models.CASCADE)
    acc_uid = models.ForeignKey(User,related_name='acc_user',on_delete=models.CASCADE)
    
class Posts(models.Model):
    image=models.FileField(upload_to='posts/')
    uid=models.ForeignKey(User,related_name='post_user',on_delete=models.CASCADE)
    title=models.CharField(max_length=100)


class Like(models.Model):
    pid = models.ForeignKey(Posts,related_name='postid',on_delete=models.CASCADE)
    user_who_like = models.ForeignKey(User,related_name='user_who_like',on_delete=models.CASCADE)

def like_notify(sender,instance, **kwargs):
    print('iam in',instance.pid.uid)
    notify.send(instance.pid.uid, recipient=instance.user_who_like, verb=("You signed in"))

post_save.connect(like_notify,sender=Like)


class Saved(models.Model):
    pid = models.ForeignKey(Posts,related_name='postId_saved',on_delete=models.CASCADE)
    user_who_save = models.ForeignKey(User,related_name='user_saved',on_delete=models.CASCADE)
    user_who_own = models.ForeignKey(User,related_name='user_own',on_delete=models.CASCADE)

class Rooms(models.Model):
    room_name = models.TextField()
    sender = models.TextField()
    receiver = models.TextField()

class ChatMessages(models.Model):
    room_name = models.ForeignKey(Rooms,related_name='roomname',on_delete=models.CASCADE)
    sender = models.TextField()
    receiver = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)
    message = models.TextField()



class Notification(models.Model):
    sender = models.TextField()
    receiver = models.TextField()
    notify = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    roomid = models.ForeignKey(Rooms,related_name='roomid',on_delete=models.CASCADE)




