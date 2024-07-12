from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponseNotFound
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import logout

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

from .serializers import KidSerializer
from core.models import Kid, StatusChange


def home(request):
    return render(request, 'api/index.html')


class NumbersView(View):
    def get(self, request):
        kids = Kid.objects.filter(Q(status='IN') | Q(status='SE') | Q(status='DE')).order_by('number').values_list('number', 'status')
        last_kid = int(kids.last()[0])
        kids = dict(kids)
        in_sum = Kid.objects.filter(Q(status='IN') | Q(status='SE')).count()
        delivered_sum = Kid.objects.filter(status="DE").count()
        numbers_list = []
        inner_list = []
        for number in range(101, last_kid+1):
            try:
                status = kids[str(number)]
            except:
                status = 'NO'
            inner_list.append((number, status))

            if number % 10 == 0:
                numbers_list.append(inner_list)
                inner_list = []
        numbers_list.append(inner_list)

        return render(
            request,
            'api/numbers.html',
            context={
                'kids': kids,
                'in_sum': in_sum,
                'delivered_sum': delivered_sum,
                'range1': [str(i) for i in range(101, 200)],
                'range2': [str(i) for i in range(201, 300)],
                'range3': [str(i) for i in range(201, 300)],
                'nums': numbers_list
            }
        )


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


class NezamatView(View):
    def get(self, request, gender):
        if not (gender == 'MA' or gender == 'FE'):
            return HttpResponseNotFound()
        if not settings.API:
            site = request.get_host()
            if 'localhost' in site:
                site = f'http://{site}'
            else:
                site = f'https://{site}'
        else:
            site = settings.API

        return render(request, 'api/nezamat.html', context={'site': site, 'gender': gender})


class NezamatView(View):
    def get(self, request):
        if not settings.API:
            site = request.get_host()
            if 'localhost' in site:
                site = f'http://{site}'
            else:
                site = f'https://{site}'
        else:
            site = settings.API

        return render(request, 'api/nezamat.html', context={'site': site})


class SendKidView(View):
    def get(self, request, gender):
        if not (gender == 'MA' or gender == 'FE'):
            return HttpResponseNotFound()
        if not settings.API:
            site = request.get_host()
            if 'localhost' in site:
                site = f'http://{site}'
            else:
                site = f'https://{site}'
        else:
            site = settings.API

        return render(request, 'api/send.html', context={'site': site, 'gender': gender})


class DeliverKidView(View):
    def get(self, request, gender):
        if not (gender == 'MA' or gender == 'FE'):
            return HttpResponseNotFound()
        if not settings.API:
            site = request.get_host()
            if 'localhost' in site:
                site = f'http://{site}'
            else:
                site = f'https://{site}'
        else:
            site = settings.API

        return render(request, 'api/deliver.html', context={'site': site, 'gender': gender})


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
        resets = {
            'gender': 'جنسیت',
            'number': 'شماره',
        }
        return render(request, 'api/reset.html', context={'resets': resets,})

    def post(self, request):
        gender = 'NO' if request.POST.get('gender', None) else None
        number = '000' if request.POST.get('number', None) else None
        password = request.POST.get('pass', '')
        if password == 'sagggggg':
            data = dict.fromkeys(['gate_in', 'gate_out', 'status',], 'NO')
            if gender: data['gender'] = gender
            if number: data['number'] = number
            data['last_change'] = None
            Kid.objects.all().update(**data)
            return redirect('https://google.com')
        else:
            return redirect('api:reset')


class ChangeStatusView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            id = int(request.data.get('id', None))
            status = request.data.get('status', None)

            if not id or not status:
                return Response(data={'success': False, 'error': 'no id or status'}, status=400)

            k = Kid.objects.get(id=id)
            previous_status = k.status
            k.status = status
            k.last_change = timezone.now()
            k.save()

            data = {
                "kid": k,
                "previous_status": previous_status,
                "status": status
            }
            if not request.user.is_anonymous: data['user'] = request.user

            StatusChange.objects.create(**data)

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


def logout_view(request):
    next = request.GET.get('next', 'api:nezamat')
    logout(request)
    return redirect(next);
