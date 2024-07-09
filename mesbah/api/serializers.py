from rest_framework import serializers

from core.models import Kid


class KidSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Kid
        fields = '__all__'

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
