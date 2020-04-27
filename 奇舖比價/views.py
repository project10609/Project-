from django.shortcuts import render
from feedback.forms import FeedbackForm
from feedback.models import Feedback
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def contact_us(request):
    feedback = Feedback.objects.all()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.name = request.POST.get('name',None)
            comment.email = request.POST.get('email',None)
            comment.feedback = request.POST.get('feedback',None)
            comment.save()
            messages.success(request,"回饋新增成功")
            return HttpResponseRedirect(reverse('contact_us'))
    else:
        form = FeedbackForm()


    return render(request,'contact_us.html',{'form':form})
