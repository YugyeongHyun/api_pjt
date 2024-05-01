from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Complete"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(APIView):
    def get(self, request, username):
        user = request.user
        if user.is_authenticated and user.username == username:
            data = {
                "username": user.username,
                "email": user.email,
                "nickname": user.nickname,
                "birthday": user.birthday,
                "gender": user.gender,
                "bio": user.bio,
            }
            return Response(data)
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
