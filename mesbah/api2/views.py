from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone

from .serializers import KidSerializer
from core.models import Kid


class KidsView(generics.ListCreateAPIView):
    serializer_class = KidSerializer
    authentication_classes = ()

    def get_queryset(self):
        gender = self.request.GET.get('gender', None)
        status = self.request.GET.get('status', None)

        qs = Kid.objects.all()
        if gender: qs = qs.filter(gender=gender)
        if status: qs = qs.filter(status=status)

        return qs


class ChangeStatusView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            id = int(request.data.get('id', None))
            status = request.data.get('status', None)

            if not id or not status:
                return Response(data={'success': False, 'error': 'no id or status'}, status=400)

            Kid.objects.filter(id=id).update(status=status, last_change=timezone.now())

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class BoysEntryView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            id = int(request.data.get('id', None))
            number = request.data.get('number', None)
            gender = request.data.get('gender', 'NO')

            if not id or number == '000' or not number:
                return Response(data={'success': False, 'error': 'no id or number'}, status=400)
            if not(gender == 'FE' or gender == 'MA'):
                return Response(data={'success': False, 'error': 'no gender'}, status=400)

            Kid.objects.filter(id=id).update(number=number, gender=gender, status='IN', last_change=timezone.now())

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class GirlsEntryView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            id = int(request.data.get('id', None))
            number = request.data.get('number', None)
            gender = request.data.get('gender', 'NO')

            if not id or number == '000' or not number:
                return Response(data={'success': False, 'error': 'no id or number'}, status=400)
            if not(gender == 'FE' or gender == 'MA'):
                return Response(data={'success': False, 'error': 'no gender'}, status=400)

            Kid.objects.filter(id=id).update(number=number, gender=gender, status='IN', last_change=timezone.now())

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class FatherDeliveryView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            id = int(request.data.get('id', None))

            if not id:
                return Response(data={'success': False, 'error': 'no id'}, status=400)

            Kid.objects.filter(id=id).update(status='RE', gate_out='MA', last_change=timezone.now())

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class MohterDeliveryView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            id = int(request.data.get('id', None))

            if not id:
                return Response(data={'success': False, 'error': 'no id'}, status=400)

            Kid.objects.filter(id=id).update(status='RE', gate_out='FE', last_change=timezone.now())

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class PorslineWebhook(APIView):
    authentication_classes = ()

    def post(self, request):
        data = request.data
        return Response(data)
