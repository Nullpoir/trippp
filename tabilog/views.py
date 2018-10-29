from django.shortcuts import render,HttpResponseRedirect
from .forms import TabilogPostingForm
from django.contrib.auth.decorators import login_required
from tabilog.models import tabilog
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .parser import parse
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

def tabilog_update(request,user_pk,tabilog_pk):
    req_user = request.user

    if req_user.pk == user_pk or req_user.is_superuser:
        if request.method != "POST":
            my_post=tabilog.objects.get(pk=tabilog_pk)
            form_context={
                "title":my_post.title,
                "body":my_post.body
            }

            edit_form=TabilogPostingForm(form_context)
            context={"form":edit_form}
            return render(request,"tabilog/postform.html",context)
        else:
            if request.POST["action"] == "confirm":
                context={"form":TabilogPostingForm(request.POST)}
                return render(request,"tabilog/postform_confirm.html",context)
            elif request.POST["action"] == "send":
                username=User.objects.get(pk=request.user.id).nickname
                my_post=tabilog.objects.get(pk=tabilog_pk)
                my_post.title=request.POST["title"]
                my_post.body=request.POST["body"]
                my_post.content=parse(request.POST["body"])
                my_post.save()

                return HttpResponseRedirect("/tabilog/post_done")
            elif request.POST["action"] == "modify":
                context={"form":TabilogPostingForm(request.POST)}
                return render(request,"tabilog/postform.html",context)

    else:
        return HttpResponseRedirect("/account/login")

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
            new_tabilog = tabilog(title=request.POST["title"],author=username,user_pk=request.user.id,body=request.POST["body"],content=parse(request.POST["body"]))
            new_tabilog.save()

            return HttpResponseRedirect("/tabilog/post_done")
        elif request.POST["action"] == "modify":
            context={"form":TabilogPostingForm(request.POST)}
            return render(request,"tabilog/postform.html",context)

    else:
        context={"form":TabilogPostingForm()}
        return render(request,"tabilog/postform.html",context)

def tabilog_delete(request):
    pass
