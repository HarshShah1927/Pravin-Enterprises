from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Product


@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.filter(is_active=True)
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'discount_price': float(p.discount_price) if p.discount_price else None,
            'stock': p.stock,
        })
    return Response(data)
