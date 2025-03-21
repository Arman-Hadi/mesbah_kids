from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken

from django.utils import timezone

from .serializers import KidSerializer, AuthTokenSerializer
from core.models import Kid, StatusChange

from datetime import date
import requests


class AddKidView(generics.CreateAPIView):
    serializer_class = KidSerializer
    authentication_classes = ()


class KidsView(generics.ListCreateAPIView):
    serializer_class = KidSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        gender = self.request.GET.get('gender', None)
        status = self.request.GET.get('status', None)

        qs = Kid.objects.all()
        if gender: qs = qs.filter(gender=gender)
        if status: qs = qs.filter(status=status)
        qs = qs.order_by('-last_change')

        return qs


class ChangeStatusView(APIView):
    authentication_classes = ()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

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


class KidsEntryView(APIView):
    authentication_classes = ()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def post(self, request, kids):
        if kids == 'boys':
            gate_in = 'MA'
        elif kids == 'girls':
            gate_in = 'FE'
        else:
            return Response(data={'error': 'endpoint not found'}, status=404)

        try:
            id = int(request.data.get('id', None))
            number = request.data.get('number', None)
            gender = request.data.get('gender', 'NO')

            if not id or number == '000' or not number:
                return Response(data={'success': False, 'error': 'no id or number'}, status=400)
            if not(gender == 'FE' or gender == 'MA'):
                return Response(data={'success': False, 'error': 'no gender'}, status=400)

            Kid.objects.filter(id=id).update(
                gate_in=gate_in, number=number, status='IN', gender=gender, last_change=timezone.now()
            )

            # Status Change
            data = {
                "kid_id": id,
                "previous_status": 'NO',
                "status": 'IN',
                "user": request.user
            }
            StatusChange.objects.create(**data)

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class ParentDeliveryView(APIView):
    authentication_classes = ()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def post(self, request, parent):
        if parent == 'father':
            gate_out = 'MA'
        elif parent == 'mother':
            gate_out = 'FE'
        else:
            return Response(data={'error': 'endpoint not found'}, status=404)

        try:
            id = int(request.data.get('id', None))

            if not id:
                return Response(data={'success': False, 'error': 'no id'}, status=400)

            Kid.objects.filter(id=id).update(
                status='RE', gate_out=gate_out, last_change=timezone.now()
            )

            # Status Change
            data = {
                "kid_id": id,
                "previous_status": 'IN',
                "status": 'RE',
                "user": request.user
            }
            StatusChange.objects.create(**data)

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class GetPorslineData(APIView):
    authentication_classes = ()

    def get(self, request):
        url = 'https://survey.porsline.ir/api/surveys/524056/responses/'
        # yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        today = str(date.today())
        payload = {
            "from_date": today,
            # "to_date": "2022-01-02",
        }
        headers = {
            'Authorization': 'API-Key 36bfd2b3b1b7b1b4dcf1da7ae833a896450a07a0',
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()['body']

            for i in data:
                porsline_id = i['data'][0]
                if Kid.objects.filter(porsline_id=porsline_id).count() == 0:    
                    prop = {
                        'porsline_id': porsline_id,
                        'first_name': i['data'][1],
                        'last_name': i['data'][2],
                        'birth_date': i['data'][3],
                        'caretaker': i['data'][4],
                        'caretaker_name': i['data'][5],
                        'caretaker_phone_number': i['data'][6],
                        'emergancy_calls': i['data'][7],
                        'wc': i['data'][8] != 'خیر',
                        'caretaker_home_number': i['data'][9],
                    }
                    Kid.objects.create(**prop)

            return Response({'success': True,})
        else:
            return Response({'error': response.text,}, status=response.status_code)


class UndoStatusView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def post(self, request):
        id = int(request.data.get('id', None))
        status = request.data.get('status', None)

        if not id or not status:
            return Response(data={'success': False, 'error': 'no id or no status'}, status=400)
        data = {
            'status': status,
        }
        if status == 'NO':
            data['last_change'] = None
            data['gate_in'] = 'NO'
            data['gate_out'] = 'NO'
            data['number'] = '000'
        elif status == 'IN':
            data['gate_out'] = 'NO'

        try:
            k = Kid.objects.filter(id=id)
            previous_status = k.values('status')[0]['status']
            k.update(**data)

            # Status Change
            data = {
                "kid_id": id,
                "previous_status": previous_status,
                "status": status,
                "user": request.user
            }
            StatusChange.objects.create(**data)

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)


class CreateAuthToken(ObtainAuthToken):
    """Create token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
