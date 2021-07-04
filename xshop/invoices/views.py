import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.template.loader import render_to_string
from django.contrib import messages

from ..orders.models import OrderItem
from .models import Invoice


# Custom administrarion
@staff_member_required
def admin_invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    order_items = OrderItem.objects.filter(order=invoice.order)
    if (
        request.user == invoice.user
        or request.user.is_superuser
        or request.user.shop == invoice.order.shop
    ):
        return render(
            request,
            "invoices/admin/invoice/detail.html",
            {"invoice": invoice, "order_items": order_items},
        )
    messages.error(
        request,
        "you do not have access to this invoice",
    )
    return redirect(reverse("admin:invoices_invoice_changelist"))


@staff_member_required
def admin_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    order_items = OrderItem.objects.filter(order=invoice.order)
    total = sum(item.total_price for item in order_items.all())
    if (
        request.user == invoice.user
        or request.user.is_superuser
        or request.user.shop == invoice.order.shop
    ):
        html = render_to_string(
            template_name="invoices/admin/invoice/pdf.html",
            context={"invoice": invoice, "order_items": order_items, "total": total},
        )
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"filename=invoice_{invoice.id}.pdf"
        weasyprint.HTML(string=html).write_pdf(
            response, font_config=weasyprint.fonts.FontConfiguration()
        )
        return response
    messages.error(
        request,
        "you do not have access to this invoice",
    )
    return redirect(reverse("admin:invoices_invoice_changelist"))
