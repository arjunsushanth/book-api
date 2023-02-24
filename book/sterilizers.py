from  rest_framework import serializers
from book.models import Books,Carts,Review
from django.contrib.auth.models import User
class Bookserializers(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    bookname=serializers.CharField()
    price=serializers.IntegerField()
    auther=serializers.CharField()
    image=serializers.ImageField()

class Modelserilizer(serializers.ModelSerializer):
    class Meta:
        model=Books
        fields='__all__'
class Userserilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]

    def create(self, validated_data):
        return  User.objects.create_user(**validated_data)
class Cartserilizer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    bookname=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields="__all__"
class ReviewSerilizer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"















