from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "message": "Welcome to Pravin Enterprises API",
        "endpoints": {
            "admin": "/admin/",
            "accounts": "/api/accounts/",
            "products": "/api/shop/",
            "cart": "/api/cart/",
            "orders": "/api/orders/",
        },
    })
