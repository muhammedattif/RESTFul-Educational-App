from .serializers import ContactUsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import ContactUs

class ContactUsView(APIView):

    permission_classes = ()

    def get(self, request):
        contact_info = ContactUs.objects.first()
        serializer = ContactUsSerializer(contact_info, many=False)
        return Response(serializer.data)
