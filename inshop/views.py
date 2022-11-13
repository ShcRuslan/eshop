from .models import *
from rest_framework import generics
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from inshop.serializers import UserRegisterSerializer, ProductSerializer, CategorySerializer, CommentSerializer, \
    CartSerializer, CartItemSerializer, OrderSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Category.objects.all()


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Comment.objects.all()


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(is_order=False, user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Cart.objects.all()


class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CartItem.objects.all()


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CartItem.objects.all()


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.validated_data["cart"]
            cart.is_order = True
            cart.save()
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


