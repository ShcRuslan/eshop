from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_price(self, obj):
        cart_id = obj.cart.id
        cart_items = CartItem.objects.filter(cart=cart_id)
        total_price = 0

        for item in cart_items:
            if item.product.discount > 0:
                total_price += (
                    item.cart_item_price - item.cart_item_price * item.product.discount
                )
            else:
                total_price += item.cart_item_price
        return total_price


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_price(self, obj):
        cart_id = obj.cart.id
        cart_items = CartItem.objects.filter(cart=cart_id)
        total_price = 0

        for item in cart_items:
            if item.product.discount > 0:
                total_price += (
                    item.cart_item_price - item.cart_item_price * item.product.discount
                )
            else:
                total_price += item.cart_item_price
        return total_price


def create(validated_data):
    user = User.objects.create(
        email=validated_data["email"],
        username=validated_data["username"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
    )
    user.set_password(validated_data["password"])
    user.save()
    return user


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True},
        }
