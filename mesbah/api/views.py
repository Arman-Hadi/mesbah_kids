from django.shortcuts import render

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from .serializers import KidSerializer
from core.models import Kid


class KidsView(generics.ListCreateAPIView):
    serializer_class = KidSerializer
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        gender = self.request.GET.get('gender', None)
        status = self.request.GET.get('status', None)

        qs = Kid.objects.all()
        if gender: qs = qs.filter(gender=gender)
        if status: qs = qs.filter(status=status)

        return qs
