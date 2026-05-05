from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from orders.models import Order
from .models import Invoice


@login_required(login_url='login')
@require_http_methods(["GET"])
def download_invoice_view(request, order_id):
    """Download invoice PDF."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    try:
        invoice = order.invoice
        return FileResponse(invoice.pdf_file.open('rb'), content_type='application/pdf')
    except Invoice.DoesNotExist:
        messages.error(request, 'Invoice not found.')
        return redirect('order-detail', order_id=order.id)
