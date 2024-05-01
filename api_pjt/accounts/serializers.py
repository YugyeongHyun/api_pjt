from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import User


class ResigisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        # 이메일에 대한 중복 검증
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],)
    password2 = serializers.CharField(  # 비밀번호 확인을 위한 필드
        write_only=True,
        required=True,
    )
    nickname = serializers.CharField(required=True)
    birthday = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'password2', 'nickname', 'birthday')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password didn't match."})
        return data

    def create(self, validated_data):
        validate_password.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            birthday=validated_data['birthday'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return user
