from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http.response import JsonResponse,HttpResponseNotFound
from .models import Image
# Create your views here.

@csrf_protect
def PostImageHandler(request):
    if request.FILES:
        upload_image = Image()
        upload_image.image=request.FILES["file"]
        upload_image.owner=request.user.id
        upload_image.save()
        upload_image.name="/media/"+upload_image.image.name
        upload_image.save()
        json={ "location" : '/media/'+upload_image.image.name }
        return JsonResponse(json)
    else:
        return HttpResponseNotFound("<h1>404</h1>")
