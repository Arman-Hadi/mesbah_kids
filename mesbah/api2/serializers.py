from rest_framework import serializers

from core.models import Kid


class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = '__all__'

    def create(self, validated_data):
        kid = Kid.objects.create(**validated_data)
        return kid
