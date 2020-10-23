from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Invoice

from .serializers import InvoiceSerializer


class InvoiceListCreateApi(APIView):
    serializer_class = InvoiceSerializer

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = self.serializer_class(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_invoice = serializer.save()
        return Response(self.serializer_class(new_invoice).data)
