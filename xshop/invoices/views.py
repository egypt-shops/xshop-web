from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from .models import Invoice
from ..orders.models import OrderItem


@staff_member_required
def admin_invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    order_items = OrderItem.objects.filter(order=invoice.order)
    return render(
        request,
        "admin/invoices/invoice/detail.html",
        {"invoice": invoice, "order_items": order_items},
    )
