from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from django.db.models import Q


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['id'] = user.id
        token['is_staff'] = user.is_staff
        # ...
       
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def userSignup(request):

    if request.method == 'POST':
        print('say helo')
        print(request.data)

        if User.objects.filter(Q(username=request.data['username']) | Q(phone=request.data['phone']) ):
            print('useralread')
            return Response(data={'error':'user is already exist'},status=409)
        serializer = UserSerializers(data=request.data,partial=True)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data,status=201)
    return Response(serializer.errors,status=400)

#google signin

@api_view(['POST'])
def google_signin(request):
    if request.method == 'POST':
        print('google')
        if User.objects.filter(username=request.data['username']):
            user = User.objects.get(username=request.data['username'])
            content={
                'username':user.username,
                'id':user.id
            }
            return Response(content,status=200)
        else:
            print(request.data)
            serializer = UserSerializers(data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=request.data['username'])

                
                
                content={
                    'id':user.id,
                    'username':user.username,
                }
                return Response(content,status=201)
    return Response(serializer.errors,status=400)
        

@api_view(['GET'])
def post(request,id):
    if request.method == 'GET':
        data = Proposal.objects.filter(uid=id)
        serializer = ProposalSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST','GET'])
def proposal(request):
    if request.method == 'POST':
        print('iamin',request.data)
        serializer = ProposalSerializer(data=request.data)
        print("checkme",serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=201)
    
        
    return Response(serializer.errors,status=400)



@api_view(['POST','GET'])
def register_mentor(request):
    if request.method == 'POST':
        dict = request.data.copy()
        dict['is_staff'] = True
        print("iamstaff",dict)
        serializer = MentorSerializer(data=dict)
        
        print("iamserilaizer",serializer.is_valid())
        print("iamserilaizer",serializer.errors)
        if serializer.is_valid():
            serializer.save()
            data = User.objects.get(username=request.data['username'])
        
            serializers = DetailSerializer(data={'address':request.data['address'],'country':request.data['country'],'state':request.data['state'],'uid':data.id})    
            if  serializers.is_valid():
                serializers.save()
                content={
                'status':201,
                'data':[serializer.data,serializers.data]
            }
                return Response(content)
    return Response(status=400)


@api_view(['GET'])
def mentor_list(request):
  
        try:
             data = User.objects.filter(is_staff=True)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = MentorSerializer(data,many=True)
            return Response(serializer.data)

#image 
@api_view(['POST','GET'])
def profileImage(request,id):
    if request.method == 'GET':
        if ProfileImage.objects.filter(uid=id):
            data = ProfileImage.objects.get(uid=id)
            serializer = ProfileImageSerializer(data)
            return Response(serializer.data)
            
        # if User.objects.filter(id=id):
        #     data = User.objects.get(id=id)
        #     serializer = UserSerializers(data)
        #     return Response(serializer.data)
    if request.method == 'POST':
        
        serializer = ProfileImageSerializer(data=request.data)
        print('myimage',serializer.is_valid())
        print('iamerror',serializer.errors)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=201)
    return Response(status=400)
@api_view(['POST'])
def change_profile(request,id):
    try:
        profile = ProfileImage.objects.get(uid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='POST':
        profile.delete()
        print('helo')
        serializer = ProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=201)
    return Response(status=400)


  #request to verify

@api_view(['POST','GET'])  
def request_to_verify(request):
    print("iqmfial",request.data)
    if request.method == 'GET':
        data = UserRequest.objects.filter(approve=False)
        serializer = RequestToVerifySerializer(data,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        print('iamthesorry')
        serializer = RequestToVerifySerializer(data=request.data)
        print('sooru',serializer.is_valid())
        print('error',serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)


@api_view(['PUT'])
def request_verify(request,id):
    try:
        req = UserRequest.objects.get(id=id)
       
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        user =User.objects.get(id=req.uid_id)
        dict={
            'verified': True
        }
       
       
        serializer = RequestToVerifySerializer(req,data=request.data,partial=True)
        userSerializer = UserSerializers(user,data=dict,partial=True)
        # print('valid',userSerializer.is_valid())
        # print('validsta',userSerializer.validated_data)
        # print(userSerializer.errors)
        if userSerializer.is_valid():
            userSerializer.save()
        if serializer.is_valid():
            serializer.save()
            user.verified = True
            user.save()
            data = UserRequest.objects.filter(approve=False)
            serializer = RequestToVerifySerializer(data,many=True)
            print("my",serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)


# follow function
@api_view(['GET'])
def all_users(request):
    try:
        users = User.objects.exclude(is_superuser=True)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        serializer = UserListSerializer(users,many=True)
        return Response(serializer.data,status=201)
    return Response(status=400)

@api_view(['GET'])
def users(request):
    try:
        user = User.objects.filter(verified=False,is_staff=False)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        print('ioo')
        print('users list',user)
        serializer = UserSerializers(user,many=True)
        return Response(serializer.data,status=201)
    return Response(status=400)


@api_view(['GET'])
def userList(request):
    # print('iamuserList')
    try:
        user = User.objects.filter(verified=True)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserListSerializer(user,many=True)
       
        return Response(serializer.data,status=201)
    return Response(status=400)

@api_view(['GET'])
def userCheck(request,id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializers(user)
        return Response(serializer.data)
    return Response(status=400)

@api_view(['GET'])
def usersDetailView(request,id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserListSerializer(user)
        return Response(serializer.data)
    return Response(status=400)

@api_view(['POST','GET'])
def postCreate(request):
    print('iampostcreate')
    if request.method == 'POST':    
        serializer = PostSerializer(data=request.data)
        print('serializer',serializer.is_valid())
        print('errpr',serializer.errors)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=201)
    return Response(status=400)
    
@api_view(['POST','GET'])
def postget(request,id):
    try:
        post = Posts.objects.filter(uid=id)
    except:
         return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)
    return Response(status=400)

@api_view(['GET'])
def posts(request):
    try:
        post = User.objects.filter(verified=True)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        
        serializer = UserListSerializer(post,many=True)
        dict = serializer.data.copy()
       
        return Response(serializer.data)
    return Response(status=400)

@api_view(['POST'])
def follow_user(request,id):
    if request.method == 'POST':
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            fol = follow.objects.filter(acc_uid=id)
            ser = FollowSerializer(fol,many=True)
            return Response(ser.data,status=201)
    return Response(status=400)

@api_view(['DELETE'])
def unfollow(request,id,uid):
    print('iamin',request.data)
    try:
        data = follow.objects.filter(acc_uid=uid,f_uid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        print('data',data)
        data.delete()
        fol = follow.objects.filter(acc_uid=uid)
        ser = FollowSerializer(fol,many=True)
        return Response(ser.data,status=200)
    return Response(status=400)



@api_view(['GET'])
def follow_get(request,id):
    try:
        data = follow.objects.filter(acc_uid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print('followin')
        serializer = FollowingSerializer(data,many=True)
       
        return Response(serializer.data)
    return Response(status=400)

@api_view(['GET'])
def follow_gets(request,id):
    try:
        data = follow.objects.filter(acc_uid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print('followin')
        serializer = FollowingSerializer(data,many=True)
        print('serializer.data')
        return Response(serializer.data,status=200)
    return Response(status=400)

@api_view(['GET'])
def followers_get(request,id):
    try:
        data = follow.objects.filter(f_uid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print('datafilter',data)
        serializer = FollowersSerializer(data,many=True)
        # print('serializer.dataget',serializer.is_valid())
        # print('serializer.dataerror',serializer.errors)
        return Response(serializer.data,status=200)
    return Response(status=400)

# saved post

@api_view(["POST"])
def saved(request):
    if request.method == 'POST':
        serializers = SavedSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=200)
    return Response(status=400)

@api_view(['GET'])
def savedget(request,id):
    try:
        print(';saved ois ',id)
        data = Saved.objects.filter(user_who_save=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print('iam in saved post get')
        serializer = SavedSerializer(data,many=True)
        return Response(serializer.data,status=200)
    return Response(status=400)

# to check saved or not,unsave
@api_view(['GET','DELETE'])
def check_saved(request,pid,id):
    # try:
    #     data = Saved.objects.filter(user_who_save=id,pid=pid)
    # except:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        if Saved.objects.filter(user_who_save=id,pid=pid):
            data = Saved.objects.filter(user_who_save=id,pid=pid)
            print('saved check',data)
            serializer = SavedSerializer(data,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if Saved.objects.filter(user_who_save=id,pid=pid):
            data = Saved.objects.filter(user_who_save=id,pid=pid)
            data.delete()
            return Response(status=202)

    return Response(status=400)


@api_view(['GET','POST','DELETE'])
def like(request,id,uid):
    if request.method == 'GET':
        print('like',id,uid)
        if Like.objects.filter(pid=id,user_who_like=uid):
            post = Like.objects.filter(pid=id,user_who_like=uid)
       

            serializer = LikeSerializer(post,many=True)
            print(serializer.data)
            return Response(serializer.data,status=200)
        else:
            return Response(status=404)
    if request.method == 'POST':
        print('iam in like')
        if Like.objects.filter(pid=id,user_who_like=uid):
            pass
        else:
            serializer = LikeSerializer(data=request.data)
            # print('is valid',serializer.is_valid())
            # print('is error',serializer.errors)
            if serializer.is_valid():
                serializer.save()
                # count = Like.objects.filter(pid=id)
                return Response(serializer.data,status=201)
    if request.method == 'DELETE':
        if Like.objects.filter(pid=id,user_who_like=uid):
            like = Like.objects.filter(pid=id,user_who_like=uid)
            like.delete()
            return Response(status=202)
    return Response(status=400)

# @api_view(['GET'])
# def saved_get(request,id):
#     try:
#         data = Saved.objects.filter(user_who_save=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = SavedSerializer(data,many=True)
#         return Response(serializer.data,status=201)
#     return Response(status=400)


@api_view(['GET'])
def like_count(request,id):
    if request.method == 'GET':
        if Like.objects.filter(pid=id):
            count = Like.objects.filter(pid=id)
        
            serializer = LikeSerializer(count,many=True)
            return Response(serializer.data,status=200)

    
    return Response(status=400)

# notification

@api_view(['POST','GET'])
def notify(request):
    if request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
   
    return Response(status=400)

@api_view(['POST','GET'])
def notify_get(request,id):
    try:
        data = Notification.objects.filter(receiver=id).order_by('-created_at')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NotificationSerializer(data,many=True)
        print('ser',serializer.data)
        # print('valid',serializer.is_valid())
        # print('error',serializer.errors)
        # dict = {
        #     'data':serializer.data
        #   }
        return Response(serializer.data)
    return Response(status=400)

@api_view(['POST','GET'])
def create_room(request):

    data = Rooms.objects.filter(sender=request.data['sender'],receiver=request.data['receiver'])
    data2 = Rooms.objects.filter(sender=request.data['receiver'],receiver=request.data['sender'])
    if data2 or data:
            if data:
                 serializer = RoomSerializer(data,many=True)
                
            else:
                 serializer = RoomSerializer(data2,many=True)
                        
            return Response(serializer.data)
       
    else:
        if request.method == 'POST':
            serializer = RoomSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
    return Response(status=400)
@api_view(['GET'])
def get_room(request,sender,receiver):
    if Rooms.objects.filter(sender=sender,receiver=receiver):
        data = Rooms.objects.filter(sender=sender,receiver=receiver)
        serializer =RoomSerializer(data,many=True)
        return Response(serializer.data)
    return Response(status=400)

@api_view(['GET'])
def messages(request,id):
    try:
        chat = ChatMessages.objects.filter(room_name=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ChatMessageSerializer(chat,many=True)
        print('chat',serializer.data)
        return Response(serializer.data)
    return Response(status=400)





               


@api_view(['GET','POST'])
def getRoutes(request):
    print('iam in')
    routes = [
        '/api/token',
        '/api/token/refresh'

    ]
    return Response(routes)