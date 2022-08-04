from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

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
                return Response(data={'success': False, 'error': str(e)}, status=400)

            Kid.objects.filter(id=id).update(status=status)

            return Response(data={'success': True,}, status=200)
        except Exception as e:
            return Response(data={'success': False, 'error': str(e)}, status=400)
