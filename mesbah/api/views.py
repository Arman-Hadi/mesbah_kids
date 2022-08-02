from django.shortcuts import render, redirect
from django.views import View

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from .serializers import KidSerializer
from core.models import Kid


class KidsView(generics.ListAPIView):
    serializer_class = KidSerializer
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        gender = self.request.GET.get('gender', None)
        status = self.request.GET.get('status', None)

        qs = Kid.objects.all()
        if gender: qs = qs.filter(gender=gender)
        if status: qs = qs.filter(status=status)

        return qs


class FatherRequestView(View):
    def get(self, request):
        context = {'parent': 'پدر',}
        return render(request, 'api/form.html', context=context)

    def post(self, request):
        name = request.POST.get('name', '')
        number = int(request.POST.get('number', 0))
        gender = 'MA' if request.POST.get('gender', '') == 'پسر' else 'FE'
        kid = Kid.objects.create(name=name, number=number, gender=gender, parent='FA')

        return redirect('api:father')


class MotherRequestView(View):
    def get(self, request):
        context = {'parent': 'مادر',}
        return render(request, 'api/form.html', context=context)

    def post(self, request):
        name = request.POST.get('name', '')
        number = int(request.POST.get('number', 0))
        gender = 'MA' if request.POST.get('gender', '') == 'پسر' else 'FE'
        kid = Kid.objects.create(name=name, number=number, gender=gender, parent='MO')

        return redirect('api:mother')
