from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseBadRequest
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import serializers, viewsets
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import os
import shutil
# Create your views here.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'filepath', 'filterpath', 'pub_date', 'thumbnail', 'description']
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'name': obj.user.profile.name,
            'phone': obj.user.username,
        }

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = (MultiPartParser, FormParser,)
    read_only_fields = ('user',)

    def perform_create(self, serializer):
        """
        1. upload된 영상 파일을 os tape input file로 전달.
        2. os 모듈로 main.py 실행.
        3. upload 영상 filtering.
        4. filtering된 영상 db에 가져와 저장.
        5. app 화면에는 filtering된 영상 업로드.
        """
        # MemoryUploadedFile 과 TemporaryUploadedFile 처리
        raw_video = self.request.data.get('filepath').temporary_file_path()

        tape_input = os.path.join(settings.TAPE_ROOT, 'input/')

        # copy raw video into tape input directory
        os.system("cp " + raw_video + " " + tape_input + "test2.mp4")
        # shutil.copyfile(raw_video, tape_input + 'test2.mp4')

        # 상대 경로이기 때문에 cd로 해당 루트로 들어가서 실행.
        # system 첫 호출시 위치는 root.
        os.system("cd " + settings.TAPE_ROOT + " && python main.py")

        # Get reult file & save the file at filtering field
        output_path = os.path.join(settings.TAPE_ROOT, 'output/')

        result_file = "filter_" + os.listdir(output_path)[os.listdir(output_path).index('test2.mp4')]
        thumnail = "filter_" + os.listdir(output_path)[os.listdir(output_path).index('test2.jpg')]

        # copy media directory
        os.system("cp " + output_path + "test2.mp4 " + os.path.join(settings.MEDIA_ROOT, result_file))
        os.system("cp " + output_path + "test2.jpg " + os.path.join(settings.MEDIA_ROOT, thumnail))

        serializer.save(
            user=User.objects.get(pk=self.request.data.get('user')),
            title=self.request.data.get('title'),
            filepath=self.request.data.get('filepath'),
            description=self.request.data.get('description'),
            filterpath=result_file,
            thumbnail=thumnail,
            )

        # user = auth.authenticate(
        #     request, username=request.POST['phone'], password=request.POST['password'])

@csrf_exempt
def login(request):
    try:
        user = auth.authenticate(request, username=request.POST['phone'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return JsonResponse({
                'id': user.id,
            })
        raise ValueError('user not found or incorrect password!')
    except Exception as ex:
        return JsonResponse({
            'error': str(ex),
        })

@csrf_exempt
def signup(request):
    try:
        user = User.objects.create_user(username=request.POST['phone'], password=request.POST['password'])
        user.profile.name = request.POST['name']
        user.profile.passwordQuestion = request.POST['password_question']
        user.profile.passwordQuestionAnswer = request.POST['password_question_answer']
        auth.login(request, user)
        return JsonResponse({
            'id': user.id,
        })
    except Exception as ex:
        return JsonResponse({
            'error': str(ex),
        })
