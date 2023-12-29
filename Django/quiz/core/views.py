from django.shortcuts import render

from rest_framework import permissions
from rest_framework import views,status
from rest_framework.response import Response
from rest_framework.generics import *

from django.contrib.auth import login

from .serializers import *
from .permissions import *

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class CourseCreateView(CreateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CourseRetrieveView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

class QuizCreateView(CreateAPIView):

    permission_classes = (IsOwner,)
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer

class QuizRetrieveView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    lookup_url_kwarg = 'quiz_id'
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = (IsOwner,)
