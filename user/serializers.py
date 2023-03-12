from rest_framework import serializers
from .models import *
from django.forms.models import model_to_dict
import json

class UserSerializers(serializers.ModelSerializer):
    # profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username','email','phone','password','last_name','first_name','verified','googleprofile']
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        # print('psw',password)
        # print('ins',instance)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proposal
        fields=['image_one','image_two','image_three','title','describe','uid']

# class UserProposalSerializers(serializers.ModelSerializer):
#     Proposal_user = ProposalSerializer(many=True)
#     class Meta:
#         models=User
#         fields=['id','username']

class DetailSerializer(serializers.ModelSerializer):
    # user = UserSerializers(many=True)
    class Meta:
        model=Details
        fields=['uid','address','state','country']


class MentorSerializer(serializers.ModelSerializer):
    user = DetailSerializer(many=True,read_only=True)
    profile = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id','username','email','phone','password','last_name','first_name','is_staff','user','profile']
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        print('psw',password)
        print('ins',instance)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def get_profile(self,obj):
        if ProfileImage.objects.filter(uid=obj.id):
            data = ProfileImage.objects.get(uid=obj.id)
            print('mentor profile',data.dp)
            return str(data.dp)

class ProfileImageSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    class Meta:
        model=ProfileImage
        fields=['id','uid','dp','active','created_at','verified','username','first_name','last_name']
    def get_verified(self,obj):
        return obj.uid.verified
    def get_username(self,obj):
        return obj.uid.username
    def get_first_name(self,obj):
        return obj.uid.first_name
    def get_last_name(self,obj):
        return obj.uid.last_name

# request to verify
class RequestToVerifySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model=UserRequest
        fields=['name','id','email',
        'phone','address','company_name',
        'email_company','company_address','uid','username','approve']
    
    def get_username(self,obj):
        return obj.uid.username



    

class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = follow
        fields='__all__'

       
    

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()
   
    class Meta:
        model = Posts
        fields=['id','image','title','username','uid','verified']
        
    def get_username(self,obj):
        return obj.uid.username
    def get_verified(self,obj):
        return obj.uid.verified
         

class UserListSerializer(serializers.ModelSerializer):
    user_image = ProfileImageSerializer(many=True)
    post_user=PostSerializer(many=True)
    fuser = FollowSerializer(many=True)
    class Meta:
        model = User
        fields=['id','username','user_image','last_name','first_name','verified','post_user','fuser']

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['user_who_like','pid','username','profile']
    def get_username(self,obj):
        print(type(obj.user_who_like.username))
        return obj.user_who_like.username
    def get_profile(self,obj):
        if ProfileImage.objects.filter(uid=obj.user_who_like):
            p=ProfileImage.objects.get(uid=obj.user_who_like)
            
            return str(p.dp)

class FollowersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    dp = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()
    class Meta:
        model = follow
        fields = ['id','f_uid','acc_uid','username','dp','verified']
    def get_username(self,obj):
        print(type(obj.acc_uid.username))
        return obj.acc_uid.username
    def get_verified(self,obj):
        return obj.acc_uid.verified
    def get_dp(self,obj):
        try:
            p = ProfileImage.objects.get(uid=obj.acc_uid)
            return p.dp.url
        except ProfileImage.DoesNotExist:
            return None


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    dp = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()
    class Meta:
        model = follow
        fields = ['id','f_uid','acc_uid','username','dp','verified']
    def get_username(self,obj):
        print(type(obj.f_uid.username))
        return obj.f_uid.username

    def get_verified(self,obj):
        return obj.f_uid.verified
    def get_dp(self,obj):
        try:
            p = ProfileImage.objects.get(uid=obj.f_uid)
            return p.dp.url
        except ProfileImage.DoesNotExist:
            return None

        
class NotificationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['sender','receiver','is_seen','notify','username']
    def get_username(self,obj):
        return obj.sender.username

class SavedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Saved
        fields = ['id','pid','user_who_save','user_who_own','username','image','title','profile']
    def get_username(self,obj):
        return obj.user_who_own.username
    def get_image(self,obj):
       
        
        return str(obj.pid.image)
    def get_title(self,obj):
        return str(obj.pid.title)
    def get_profile(self,obj):
        if ProfileImage.objects.filter(uid=obj.user_who_own):
            d=ProfileImage.objects.get(uid=obj.user_who_own)
            return str(d.dp)
    
            # return str(data.image)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['sender','receiver','room_name','id']




class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ['sender','message']


