from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .forms import TabilogPostingForm
from django.contrib.auth.decorators import login_required
from tabilog.models import tabilog
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .parser import parse,alldel,allsave
# Create your views here.
User=get_user_model()

def post_done(request):
    return render(request,"tabilog/post_done.html")


class post_history(UserPassesTestMixin,TemplateView):
    raise_exception = False
    template_name="tabilog/post_history.html"
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['user_pk'] or user.is_superuser

    def get(self, request, user_pk):
        my_post=tabilog.objects.all().filter(user_pk=user_pk)
        paginator=Paginator(my_post,1)
        page = request.GET.get('page')
        tabilog_output=paginator.get_page(page)
        return self.render_to_response({"lists":tabilog_output})

def tabilog_list_show(request):
    if request.method == "POST":
        pass
    else:
        tabilog_all=tabilog.objects.all()
        paginator=Paginator(tabilog_all,10)
        page = request.GET.get('page')
        tabilog_output=paginator.get_page(page)


    return render(request,"tabilog/tabilog_list.html",{"lists":tabilog_output})

def tabilog_show(request,number):
    tabilog_render=tabilog.objects.get(pk=number)
    return render(request,"tabilog/tabilog.html",{"tabilog":tabilog_render})


@login_required
def TabilogPost(request):
    form=TabilogPostingForm(request.POST or None)
    context={'form':form}

    if request.POST:
        if request.POST and form.is_valid():
            username=User.objects.get(pk=request.user.id).nickname
            print(request.POST)
            print("parse now")
            draft=tabilog(title=request.POST["title"],author=username,user_pk=request.user.id,body=request.POST["body"],content=parse(request.POST["body"]))
            draft.save()
            return HttpResponseRedirect("/tabilog/post_done/")

    return render(request,"tabilog/postform.html",context)

def tabilog_delete(request,tabilog_pk):
    post = get_object_or_404(tabilog, pk=tabilog_pk)

    if req_user.pk == post.user_pk or req_user.is_superuser:
        alldel(post.body)
        post.delete();
        return render("aaa");
    else:
        return HttpResponseRedirect("/")

def tabilog_update(request,user_pk,tabilog_pk):
    req_user = request.user

    if req_user.pk == user_pk or req_user.is_superuser:
        post = get_object_or_404(tabilog, pk=tabilog_pk)
        alldel(post.body)
        form = TabilogPostingForm(request.POST or None, instance=post)

        if request.method == 'POST' and form.is_valid():
            post.title=request.POST["title"]
            post.body=request.POST["body"]
            post.content=parse(request.POST["body"])
            post.save()

            return HttpResponseRedirect("/tabilog/post_done/")

        context = {
            'form': form
        }

        return render(request, 'tabilog/postform.html', context)
    else:
        return HttpResponseRedirect("/account/login")
