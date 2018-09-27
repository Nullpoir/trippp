from django.shortcuts import render,HttpResponseRedirect
from .forms import TabilogPostingForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def post_done(request):
    return render(request,"tabilog/post_done.html")

@login_required
def TabilogPost(request):
    if request.method == "POST":
        if request.POST["action"] == "confirm":
            context={"form":TabilogPostingForm(request.POST)}
            return render(request,"tabilog/postform_confirm.html",context)
        elif request.POST["action"] == "send":
            return HttpResponseRedirect("/tabilog/post_done")
        elif request.POST["action"] == "modify":
            context={"form":TabilogPostingForm(request.POST)}
            return render(request,"tabilog/postform.html",context)

    else:
        context={"form":TabilogPostingForm()}
        return render(request,"tabilog/postform.html",context)
