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
