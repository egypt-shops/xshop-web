from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Invoice
from xshop.orders.models import Order
from .serializers import InvoiceSerializer
from xshop.core.utils import UserGroup


class InvoiceListCreateApi(APIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="List all invoices",
        responses={200: "Invoices list", 401: "Not Authenticated"},
    )
    def get(self, request):
        user = request.user
        if not user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.is_superuser:
            invoices = Invoice.objects.all()
            serializer = self.serializer_class(invoices, many=True)
            return Response(serializer.data)

        elif user.type and bool(
            user.type[0]
            in [
                UserGroup.GENERAL_MANAGER.title(),
                UserGroup.CASHIER.title(),
            ]
        ):
            invoices = Invoice.objects.filter(
                order__in=Order.objects.filter(shop=user.shop)
            ) | Invoice.objects.filter(user=user)
            serializer = self.serializer_class(invoices, many=True)
            return Response(serializer.data)
        elif user.type and bool(
            user.type[0]
            in [
                UserGroup.DATA_ENTRY_CLERK.title(),
                UserGroup.CUSTOMER.title(),
            ]
        ):
            invoices = Invoice.objects.filter(user=user)
            serializer = self.serializer_class(invoices, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        description="Create new invoice",
        request=InvoiceSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_invoice = serializer.save()
        return Response(self.serializer_class(new_invoice).data)


class InvoiceDetailPatchApi(APIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get invoice details",
        responses={
            200: InvoiceSerializer,
            404: "Invoice not found",
            401: "Not Authenticated",
        },
    )
    def get(self, request, invoice_id):
        try:
            if not request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            invoice = Invoice.objects.get(id=invoice_id)
            if (
                request.user == invoice.user
                or request.user.is_superuser
                or (
                    request.user.shop == invoice.order.shop
                    and bool(
                        request.user.type[0]
                        not in [
                            UserGroup.DATA_ENTRY_CLERK.title(),
                        ]
                    )
                )
            ):
                serializer = self.serializer_class(invoice, many=False)
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Patch existing invoice",
        request=InvoiceSerializer,
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
