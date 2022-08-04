from django.shortcuts import render
from hotelmenuapp.models import menu_items
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class MenuView(APIView):
    def get(self,request,*args,**kwargs):
        all_items=menu_items
        if "category" in request.query_params:
            category=request.query_params.get("category")
            all_items=[item for item in menu_items if item.get("category")==category]
        if "limit" in request.query_params:
             lim=int(request.query_params.get("limit"))
             all_items=all_items[:lim]
        return Response(data=all_items)

    # def get(self, request, *args, **kwargs):
    #     return Response(data=menu_items)

    def post(self, request, *args, **kwargs):
        data = request.data
        menu_items.append(data)
        return Response(data=data)



class MenuDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        item = [item for item in menu_items if item["code"] == id].pop()
        return Response(data=item)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        item = [item for item in menu_items if item["code"] == id].pop()
        item.update(request.data)
        return Response(data=item)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        item = [item for item in menu_items if item["code"] == id].pop()
        menu_items.remove(item)
        return Response(data=item)

