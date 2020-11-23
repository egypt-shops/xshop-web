from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import Invoice
from .serializers import InvoiceSerializer
from drf_yasg2.utils import swagger_auto_schema


class InvoiceListCreateApi(APIView):
    serializer_class = InvoiceSerializer

    @swagger_auto_schema(
        operation_description="List all invoices", responses={200: "Invoices list"},
    )
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = self.serializer_class(invoices, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create new invoice", request_body=InvoiceSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_invoice = serializer.save()
        return Response(self.serializer_class(new_invoice).data)


class InvoiceDetailPatchApi(APIView):
    serializer_class = InvoiceSerializer

    @swagger_auto_schema(
        operation_description="Get invoice details",
        responses={200: InvoiceSerializer, 404: "Invoice not found"},
    )
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)

            serializer = self.serializer_class(invoice, many=False)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Patch existing invoice",
        request_body=InvoiceSerializer,
        responses={404: "Invoice does not exist"},
    )
    def patch(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            serializer = self.serializer_class(invoice, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_invoice = serializer.save()
            return Response(self.serializer_class(updated_invoice).data)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
