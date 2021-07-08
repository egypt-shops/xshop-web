from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from ..models import Shop
from .serializers import ShopSerializer


class ShopListApi(APIView):
    serializer_class = ShopSerializer

    @extend_schema(
        description="List all shops that exists in the DB",
        responses={200: "[List of shops]"},
    )
    def get(self, request):
        shops = Shop.objects.all()
        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopDetailApi(APIView):
    serializer_class = ShopSerializer

    @extend_schema(
        description="Get specific shop's data",
        responses={200: ShopSerializer, 404: "Shop not found"},
    )
    def get(self, request, shop_subdomain):
        shop = get_object_or_404(Shop, subdomain=shop_subdomain)
        serializer = self.serializer_class(shop, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
