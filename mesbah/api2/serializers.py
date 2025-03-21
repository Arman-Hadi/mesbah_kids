from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from core.models import Kid


class KidSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Kid
        fields = '__all__'

    def create(self, validated_data):
        kid = Kid.objects.create(**validated_data)
        return kid

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class AuthTokenSerializer(serializers.Serializer):
    ''' Serializer for the user authentication '''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        user.last_login = timezone.now()
        user.save()

        attrs['user'] = user
        return attrs
