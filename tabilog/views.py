from django.shortcuts import render,HttpResponseRedirect
from .forms import TabilogPostingForm
from django.contrib.auth.decorators import login_required
from tabilog.models import tabilog
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
User=get_user_model()

def post_done(request):
    return render(request,"tabilog/post_done.html")

def tabilog_list_show(request):
    if request.method == "POST":
        pass
    else:
        tabilog_all=tabilog.objects.all()
        paginator=Paginator(tabilog_all,1)
        page = request.GET.get('page')
        tabilog_output=paginator.get_page(page)


    return render(request,"tabilog/tabilog_list.html",{"lists":tabilog_output})

def tabilog_show(request,number):
    tabilog_render=tabilog.objects.get(pk=number)
    return render(request,"tabilog/tabilog.html",{"tabilog":tabilog_render})


@login_required
def TabilogPost(request):
    if request.method == "POST":
        if request.POST["action"] == "confirm":
            context={"form":TabilogPostingForm(request.POST)}
            return render(request,"tabilog/postform_confirm.html",context)
        elif request.POST["action"] == "send":
            username=User.objects.get(pk=request.user.id).nickname
            new_tabilog = tabilog(title=request.POST["title"],author=username,body=request.POST["body"])
            new_tabilog.save()

            return HttpResponseRedirect("/tabilog/post_done")
        elif request.POST["action"] == "modify":
            context={"form":TabilogPostingForm(request.POST)}
            return render(request,"tabilog/postform.html",context)

    else:
        context={"form":TabilogPostingForm()}
        return render(request,"tabilog/postform.html",context)

def tabilog_mylist(request):
    pass
def tabilog_update(request):
    pass
def tabilog_delete(request):
    pass
