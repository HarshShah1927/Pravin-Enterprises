from io import BytesIO
import uuid

from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Invoice, InvoiceTemplate


def get_active_invoice_template():
    template = InvoiceTemplate.objects.filter(is_active=True).first()
    if template:
        return template
    return InvoiceTemplate.objects.create(is_active=True)


def generate_invoice(order, payment=None, replace=False):
    try:
        invoice = order.invoice
    except Invoice.DoesNotExist:
        invoice = None
    if invoice and not replace:
        return invoice

    template = get_active_invoice_template()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        fontName='Helvetica-Bold',
    )
    heading_style = ParagraphStyle(
        'InvoiceHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        fontName='Helvetica-Bold',
    )

    elements = [
        Paragraph(template.company_name, title_style),
        Paragraph(template.title, styles['Heading2']),
    ]
    company_lines = [template.company_address, template.company_phone, template.company_email]
    company_text = '<br/>'.join(line for line in company_lines if line)
    if company_text:
        elements.extend([Paragraph(company_text, styles['Normal']), Spacer(1, 0.2 * inch)])

    invoice_number = invoice.invoice_number if invoice else f"INV-{order.order_id}"
    invoice_data = [
        ['Invoice Number:', invoice_number, 'Invoice Date:', order.created_at.strftime('%d-%m-%Y')],
        ['Order Number:', order.order_id, 'Due Date:', order.created_at.strftime('%d-%m-%Y')],
    ]
    invoice_table = Table(invoice_data, colWidths=[1.5 * inch, 2 * inch, 1.5 * inch, 2 * inch])
    invoice_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.extend([invoice_table, Spacer(1, 0.3 * inch)])

    elements.append(Paragraph('Bill To:', heading_style))
    customer_name = order.user.get_full_name() or order.user.username
    customer_info = f"{customer_name}<br/>{order.user.email}<br/>{order.shipping_phone}<br/>{order.shipping_address}"
    elements.extend([Paragraph(customer_info, styles['Normal']), Spacer(1, 0.2 * inch)])

    items_data = [['Product Name', 'Quantity', 'Unit Price', 'Subtotal']]
    for item in order.items.select_related('product'):
        product_name = item.product.name if item.product else 'Unknown product'
        items_data.append([
            product_name,
            str(item.quantity),
            f"Rs. {item.price:.2f}",
            f"Rs. {item.subtotal:.2f}",
        ])

    items_table = Table(items_data, colWidths=[2.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
    ]))
    elements.extend([Paragraph('Order Items:', heading_style), items_table, Spacer(1, 0.2 * inch)])

    totals_data = [
        ['', '', 'Subtotal:', f"Rs. {order.subtotal:.2f}"],
        ['', '', 'Shipping:', f"Rs. {order.shipping_cost:.2f}"],
        ['', '', 'Tax:', f"Rs. {order.tax:.2f}"],
        ['', '', 'Discount:', f"Rs. {order.discount:.2f}"],
        ['', '', 'Total Amount:', f"Rs. {order.total_amount:.2f}"],
    ]
    totals_table = Table(totals_data, colWidths=[2.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e6f1')),
        ('GRID', (2, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.extend([totals_table, Spacer(1, 0.3 * inch)])

    if template.terms_and_conditions:
        elements.extend([Paragraph('Terms:', heading_style), Paragraph(template.terms_and_conditions, styles['Normal'])])
    elements.append(Paragraph(template.footer_message, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    invoice_filename = f"{invoice_number}-{uuid.uuid4().hex[:4]}.pdf"

    if not invoice:
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            order=order,
            payment=payment,
            customer_name=customer_name,
            customer_email=order.user.email,
            customer_phone=order.shipping_phone,
            subtotal=order.subtotal,
            shipping_cost=order.shipping_cost,
            tax=order.tax,
            discount=order.discount,
            total_amount=order.total_amount,
        )
    else:
        invoice.payment = payment
        invoice.customer_name = customer_name
        invoice.customer_email = order.user.email
        invoice.customer_phone = order.shipping_phone
        invoice.subtotal = order.subtotal
        invoice.shipping_cost = order.shipping_cost
        invoice.tax = order.tax
        invoice.discount = order.discount
        invoice.total_amount = order.total_amount

    invoice.pdf_file.save(invoice_filename, ContentFile(buffer.getvalue()), save=False)
    invoice.save()
    return invoice
