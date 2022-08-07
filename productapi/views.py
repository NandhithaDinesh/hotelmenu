import status as status
from django.shortcuts import render
from rest_framework.views import  APIView
from rest_framework.response import Response
from productapi.models import Products
from rest_framework import status
# Create your views here.
from productapi.serializers import ProductSerializer
from productapi.serializers import ProductModelSerializer,UserSerializer
from rest_framework.viewsets import ViewSet,ModelViewSet
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
class ProductsView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        #deserialization
        serializer=ProductSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)
class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serializer=ProductSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    # def put(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     instance=Products.objects.get(id=id)
    #     serializer=ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         instance.product_name=serializer.validated_data.get("product_name")
    #         instance.category = serializer.validated_data.get("category")
    #         instance.price = serializer.validated_data.get("price")
    #         instance.rating = serializer.validated_data.get("rating")
    #         instance.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    # another method foer update
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Products.objects.filter(id=id)
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
           instance.update(**serializer.validated_data)
           return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Products.objects.get(id=id)
        serializer=ProductSerializer(instance)
        instance.delete()
        return Response({"msg:deleted"},status=status.HTTP_204_NO_CONTENT)


class ProductModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category__contains=request.query_params.get("category"))
        if "price_gt" in request.query_params:
            qs=qs.filter(price__gte=request.query_params.get("price_gt"))
        serializer=ProductModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer=ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class ProductDetailsModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serializer=ProductModelSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        object=Products.objects.get(id=id)
        serializer = ProductModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,  *args, **kwargs):
        id=kwargs.get("id")
        instance=Products.objects.get(id=id)
        instance.delete()
        return Response({"msg:deleted"}, status=status.HTTP_204_NO_CONTENT)

class ProductViewSetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kwargs):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Products.objects.get(id=id)
        serializer=ProductModelSerializer(qs)
        return Response(data=serializer.data)
    def  update(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        object = Products.objects.get(id=id)
        serializer = ProductModelSerializer(data=request.data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        instance = Products.objects.get(id=id)
        instance.delete()
        return Response({"msg:deleted"})
class ProductModelViewSetView(ModelViewSet):
    serializer_class=ProductModelSerializer
    queryset=Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
class UserModelViewSetView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
