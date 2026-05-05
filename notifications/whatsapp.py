"""
WhatsApp notification module using Twilio.
"""

import logging

from django.conf import settings
from twilio.rest import Client

logger = logging.getLogger(__name__)


def whatsapp_is_configured():
    invalid_values = {
        '',
        'your-twilio-account-sid',
        'your-twilio-auth-token',
        'your_twilio_account_sid_here',
        'your_twilio_auth_token_here',
        'whatsapp:+91xxxxxxxxxx',
    }
    values = [
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_WHATSAPP_NUMBER,
        settings.OWNER_WHATSAPP_NUMBER,
    ]
    return all(value not in invalid_values for value in values)


def send_order_notification(order):
    """Send a new-order WhatsApp message to the store owner."""
    if not whatsapp_is_configured():
        logger.warning('WhatsApp is not configured; skipped order notification.')
        return False

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        items_text = "\n".join([
            f"- {item.product.name} x{item.quantity} - Rs. {item.subtotal:.2f}"
            for item in order.items.all()
        ])

        message_body = f"""
*New Order Placed*

*Order ID:* {order.order_id}
*Customer Name:* {order.user.get_full_name()}
*Contact Number:* {order.shipping_phone}
*Email:* {order.user.email}

*Items Ordered:*
{items_text}

*Order Total:* Rs. {order.total_amount:.2f}
*Shipping Address:*
{order.shipping_address}
{order.shipping_city}, {order.shipping_state} {order.shipping_postal_code}

*Status:* {order.order_status.capitalize()}
*Invoice:* Generated

Please review the order in the admin panel.
"""

        client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=settings.OWNER_WHATSAPP_NUMBER,
        )

        logger.info(f"WhatsApp notification sent for order {order.order_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp notification: {str(e)}")
        return False


def send_order_status_update(order, status):
    """Send an order status update to the customer."""
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        status_messages = {
            'confirmed': 'Your order has been confirmed and is being prepared.',
            'processing': 'Your order is being prepared for shipment.',
            'shipped': 'Your order has been shipped.',
            'out_for_delivery': 'Your order is out for delivery.',
            'delivered': 'Your order has been delivered.',
            'cancelled': 'Your order has been cancelled.',
        }

        message_body = f"""
Order Update for Order #{order.order_id}

{status_messages.get(status, f'Your order status: {status}')}

For more details, visit your order page or contact us.
"""

        customer_whatsapp = f"whatsapp:{order.shipping_phone}"
        client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=customer_whatsapp,
        )

        logger.info(f"WhatsApp status update sent for order {order.order_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send status update: {str(e)}")
        return False


def send_invoice_via_whatsapp(order, invoice):
    """Send invoice details via WhatsApp to the customer."""
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message_body = f"""
Invoice for Order #{order.order_id}

Invoice Number: {invoice.invoice_number}
Total Amount: Rs. {invoice.total_amount:.2f}

Your invoice has been generated.
Thank you for your purchase!
"""

        customer_whatsapp = f"whatsapp:{order.shipping_phone}"
        client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=customer_whatsapp,
        )

        logger.info(f"Invoice sent via WhatsApp for order {order.order_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send invoice: {str(e)}")
        return False
