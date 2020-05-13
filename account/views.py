from django.shortcuts import render
from account.forms import UserForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from account.models import UserProfile

# # Create your views here.
# @login_required
# def profile(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     return render(request, 'account/profile.html', {'user': user})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def register(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password2']
            first_name = user_form.cleaned_data['first_name']

            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name)
            user.set_password(user.password)
            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect(reverse('account:user_login'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'account/registration.html', {'user_form': user_form, })


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")

        else:
            print('Failed login Detected')
            message = 'Invalid Login Info'
            return render(request, 'account/login.html', {'message': message})
    else:
        return render(request, 'account/login.html', {})
