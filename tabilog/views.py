from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .forms import TabilogPostingForm,TabilogSearchForm
from django.contrib.auth.decorators import login_required
from tabilog.models import tabilog
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .parser import parse,alldel,allsave
# Create your views here.
PAGE_LIMIT=10
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
        paginator=Paginator(my_post,PAGE_LIMIT)
        page = request.GET.get('page')
        tabilog_output=paginator.get_page(page)
        return self.render_to_response({"lists":tabilog_output})

def tabilog_list_show(request):
    form=TabilogSearchForm()
    if request.method == "POST":
        return HttpResponseRedirect("/tabilog/?keywords="+request.POST["keywords"]+"&option="+request.POST["option"])

    elif "keywords" in request.GET:
        keywords=request.GET.get("keywords")
        option=request.GET.get("option")
        page = request.GET.get('page')
        context={
            "keywords":keywords,
            "option":option
        }
        keywords=keywords.replace("　"," ")
        list=keywords.split(" ")
        print(list)
        query=Q()
        form=TabilogSearchForm(context)

        if option == "title":

            for items in list:
                query.add(Q(title__icontains=items),Q.OR)

            tabilog_all=tabilog.objects.all().filter(query)
            paginator=Paginator(tabilog_all,PAGE_LIMIT)
            tabilog_output=paginator.get_page(page)
        elif option == "tag":
            for items in list:
                query.add(Q(tag__icontains=items),Q.OR)
            tabilog_all=tabilog.objects.all().filter(query)
            paginator=Paginator(tabilog_all,PAGE_LIMIT)
            tabilog_output=paginator.get_page(page)
        else:
            for items in list:
                query.add(Q(author__icontains=items),Q.OR)
            tabilog_all=tabilog.objects.all().filter(query)
            paginator=Paginator(tabilog_all,PAGE_LIMIT)
            tabilog_output=paginator.get_page(page)
        return render(request,"tabilog/tabilog_list.html",{"lists":tabilog_output,"form":form,"search_flag":1})
    else:
        tabilog_all=tabilog.objects.all()
        paginator=Paginator(tabilog_all,PAGE_LIMIT)
        page = request.GET.get('page')
        tabilog_output=paginator.get_page(page)
        return render(request,"tabilog/tabilog_list.html",{"lists":tabilog_output,"form":form,"search_flag":1})

def tabilog_show(request,number):
    tabilog_render=tabilog.objects.get(pk=number)
    return render(request,"tabilog/tabilog.html",{"tabilog":tabilog_render,"search_flag":0})


@login_required
def TabilogPost(request):
    form=TabilogPostingForm(request.POST or None)
    context={'form':form}

    if request.POST:
        if request.POST and form.is_valid():
            username=User.objects.get(pk=request.user.id).nickname
            print(request.POST)
            res=parse(request.POST["body"])
            draft=tabilog(title=request.POST["title"],author=username,user_pk=request.user.id,body=request.POST["body"],content=res[0],index=res[1],tag=request.POST["tag"])
            draft.save()
            return HttpResponseRedirect("/tabilog/post_done/")

    return render(request,"tabilog/postform.html",context)

@login_required
def tabilog_pre_delete(request,user_pk,tabilog_pk):
    context={"user_pk":user_pk,"tabilog_pk":tabilog_pk}
    return render(request,"tabilog/delete_confirm.html",context);

@login_required
def tabilog_delete(request,user_pk,tabilog_pk):
    req_user = request.user
    post = get_object_or_404(tabilog, pk=tabilog_pk)

    if req_user.pk == post.user_pk or req_user.is_superuser:
        alldel(post.body)
        post.delete()
        return render(request,"tabilog/delete_complete.html");
    else:
        return HttpResponseRedirect("/")

@login_required
def tabilog_update(request,user_pk,tabilog_pk):
    req_user = request.user

    if req_user.pk == user_pk or req_user.is_superuser:
        post = get_object_or_404(tabilog, pk=tabilog_pk)
        alldel(post.body)
        form = TabilogPostingForm(request.POST or None, instance=post)

        if request.method == 'POST' and form.is_valid():
            post.title=request.POST["title"]
            post.body=request.POST["body"]
            res=parse(request.POST["body"])
            post.content=res[0]
            post.index=res[1]
            post.tag=request.POST["tag"]
            post.save()

            return HttpResponseRedirect("/tabilog/post_done/")

        context = {
            'form': form
        }

        return render(request, 'tabilog/postform.html', context)
    else:
        return HttpResponseRedirect("/account/login")
