from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponseNotFound

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import KidSerializer
from core.models import Kid


class KidsView(generics.ListAPIView):
    serializer_class = KidSerializer
    authentication_classes = ()

    def get_queryset(self):
        gender = self.request.GET.get('gender', None)
        status = self.request.GET.get('status', None)
        exclude = self.request.GET.getlist('exclude', None)

        qs = Kid.objects.all()
        if gender: qs = qs.filter(gender=gender)
        if status: qs = qs.filter(status=status)
        if exclude:
            for i in exclude:
                qs = qs.exclude(status=i)

        return qs


class ChangeStatusView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            name = request.data.get('name', '')
            number = request.data.get('number', 0)

            kids = Kid.objects.filter(name=name, number=number)
            for kid in kids:
                kid.status = 'DE'
                kid.save()

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class NewKidView(View):
    def get(self, request):
        return render(request, 'api/new_kid.html')

    def post(self, request):
        data = dict()
        for p, pp in request.POST.items():
            if pp and p != 'csrfmiddlewaretoken':
                data[p] = pp
        kid = Kid.objects.create(**data)
        if 'wc' in data:
            kid.wc = True
        else:
            kid.wc = False
        kid.status = 'IN'
        kid.save()
        return redirect('api:newkid')


class SendKidView(View):
    def get(self, request, gender):
        if not (gender == 'MA' or gender == 'FE'):
            return HttpResponseNotFound()
        site = request.get_host()
        if 'localhost' in site:
            site = f'http://{site}'
        else:
            site = f'https://{site}'

        return render(request, 'api/send.html', context={'site': site, 'gender': gender})


class FatherRequestView(View):
    def get(self, request):
        context = {'parent': 'پدر',}
        return render(request, 'api/form.html', context=context)

    def post(self, request):
        name = request.POST.get('name', '')
        number = int(request.POST.get('number', 0))
        gender = 'MA' if request.POST.get('gender', '') == '1' else 'FE'
        kid = Kid.objects.create(name=name, number=number, gender=gender, parent='FA', status='RE')

        return redirect('api:father')


class MotherRequestView(View):
    def get(self, request):
        context = {'parent': 'مادر',}
        return render(request, 'api/form.html', context=context)

    def post(self, request):
        name = request.POST.get('name', '')
        number = int(request.POST.get('number', 0))
        gender = 'MA' if request.POST.get('gender', '') == '1' else 'FE'
        kid = Kid.objects.create(name=name, number=number, gender=gender, parent='MO', status='RE')

        return redirect('api:mother')


class ResetView(View):
    def get(self, request):
        return render(request, 'api/reset.html')

    def post(self, request):
        password = request.POST.get('pass', '')
        if password == 'sagggggg':
            Kid.objects.all().update(gender='NO', gate_in='NO', gate_out='NO', number='000', status='NO')
            return redirect('https://google.com')
        else:
            return redirect('api:reset')
