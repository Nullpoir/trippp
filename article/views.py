from django.shortcuts import render,HttpResponseRedirect
from .forms import QuestionForm
from .models import doc
from django.core.mail import send_mail
from trippp import settings
from django.template.loader import get_template

# Create your views here.

def biz_top(request):
    return render(request,'company/top.html')

def question_get(request):
    if request.method == "POST":
        if request.POST["action"] == "confirm":
            context={"form":QuestionForm(request.POST)}
            return render(request,"company/question_confirm.html",context)
        elif request.POST["action"] == "send":
            context={
            "name":request.POST["name"],
            "mail":request.POST["mail"],
            "query":request.POST["query"],
            }
            own_email=settings.EMAIL_HOST_USER
            message_template = get_template('mail_template/query_notify.txt')
            message = message_template.render(context)
            send_mail("Trippp Recieved Customer's offer", message, own_email, [own_email,])
            return HttpResponseRedirect("/company/question_done")
        elif request.POST["action"] == "modify":
            context={"form":QuestionForm(request.POST)}
            return render(request,"company/question.html",context)

    else:
        context={"form":QuestionForm()}
        return render(request,"company/question.html",context)

def doc_show(request,pk):
    db=doc.objects.get(pk=pk)
    return render(request,"company/doc.html",{"article":db})

def doc_show_ws(request,pk):
    db=doc.objects.get(pk=pk)
    return render(request,"company/doc_ws.html",{"article":db})

def q_done(request):
    return render(request,"company/question_done.html")
