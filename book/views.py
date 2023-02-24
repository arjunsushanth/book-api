from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from book.models import Books,Carts,Review
from django.contrib.auth.models import User
from book.sterilizers import Bookserializers,Modelserilizer,Userserilizer,Cartserilizer,ReviewSerilizer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import authentication,permissions


class Bookview(APIView):
    def get(self,request,*args,**kwargs):
        qs = Books.objects.all()
        serilizer = Bookserializers(qs, many=True)
        return Response(data=serilizer.data)

    def post(self, request, *args, **kwargs):
        serilizer = Bookserializers(data=request.data)
        if serilizer.is_valid():
            Books.objects.create(**serilizer.validated_data)
            return Response(data=serilizer.data)
        else:
            return Response(data=serilizer.errors)


class Bookdetails(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Books.objects.get(id=id)
        serilizer = Bookserializers(qs, many=False)
        return Response(data=serilizer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Books.objects.filter(id=id).update(**request.data)
        qs = Books.objects.get(id=id)
        serializer = Bookserializers(qs, many=False)
        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Books.objects.filter(id=id).delete()
        return Response(data='deleted')

    def delete(self, request, *args, **kwargs):
        return Response(data="delete book")

class Bookviewset(viewsets.ModelViewSet):
    serializer_class = Modelserilizer
    queryset = Books.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
     # def list(self,request,*args,**kwargs):
     #     qs=Books.objects.all()
     #     serialize=Modelserilizer(qs,many=True)
     #     return Response(data=serialize.data)
     #
     # def create(self, request, *args, **kwargs):
     #     serializer = Modelserilizer(data=request.data)
     #     if serializer.is_valid():
     #         serializer.save()
     #         return Response(data=serializer.data)
     #     else:
     #         return Response(data=serializer.errors)
     #
     # def retrieve(self, request, *args, **kwargs):
     #     id = kwargs.get('pk')
     #     qs = Books.objects.get(id=id)
     #     serializer = Modelserilizer(qs, many=False)
     #     return Response(data=serializer.data)
     #
     # def destroy(self, request, *args, **kwargs):
     #     id = kwargs.get('pk')
     #     Books.objects.filter(id=id).delete()
     #     return Response('deleted')
     #
     # def update(self, request, *args, **kwargs):
     #     id = kwargs.get('pk')
     #     obj = Books.objects.get(id=id)
     #     serializer =Modelserilizer(data=request.data, instance=obj)
     #     if serializer.is_valid():
     #         serializer.save()
     #         return Response(data=serializer.data)
     #     else:
     #         return Response(data=serializer.errors)

    @action(methods=["POST"], detail=True)
    def addto_cart(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        item = Books.objects.get(id=id)
        user = request.user
        user.carts_set.create(product=item)
        return Response(data="item add to cart")

    @action(methods=["POST"], detail=True)
    def addto_review(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get("pk")
        item = Books.objects.get(id=id)
        serilizer = ReviewSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save(product=item, user=user)
            return Response(data=serilizer.data)
        else:
            return Response(data=serilizer.errors)

    @action(methods=["GET"], detail=True)
    def review(self, request, *args, **kwargs):
        books = self.get_object()
        qs = Books.review_set.all()
        serilizer = ReviewSerilizer(qs, many=True)
        return Response(data=serilizer.data)
         # @action(methods=["GET"], detail=False)
         # def catagory(self, request, *args, **kwargs):
         #     ras = Books.objects.values_list("catagory", flat=True).distinct()
         #     return Respone(data=ras)



class Userview(viewsets.ModelViewSet):

    def create(self,request,*args,**kwargs):
        serilizer=Userserilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(data=serilizer.data)
        else:
            return Response(data=serilizer.errors)

    serializer_class =Userserilizer
    queryset =User.objects.all()

class CartView(viewsets.ModelViewSet):
    serializer_class = Cartserilizer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)
class ReviewDeleteView(APIView):
    def delete(self,request,*args,**kwargs):
         id=kwargs.get("pk")
         Review.objects.filter(id=id).delete()
         return Response(data="deletereview")








