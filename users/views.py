from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
#the upone is used for creating of it self now we are doing an extension so make it registaration >
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if(request.method == 'POST'):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your Account has been created for {username}! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form': form })
# def register(request):
#     if request.method == 'POST':
#             form = UserRegisterForm(request.POST)
#             p_reg_form = ProfileRegisterForm(request.POST)
#             if form.is_valid() and p_reg_form.is_valid():
#                      user = form.save()
#                      user.refresh_from_db()  # load the profile instance created by the signal
#                      p_reg_form = ProfileRegisterForm(request.POST, instance=user.profile)
#                      p_reg_form.full_clean()
#                      p_reg_form.save()
#                      messages.success(request, f'Your account has been sent for approval!')
#                      return redirect('login')
#     else:
#         form = UserRegisterForm()
#         p_reg_form = ProfileRegisterForm()
#         context = {
#                'form': form,
#                'p_reg_form': p_reg_form
#             }
#     return render(request, 'users/register.html', context)



@login_required
def profile(request):
     if(request.method == 'POST'):
       u_form = UserUpdateForm(request.POST,instance=request.user)
       p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
       if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request,f'Your Account has been updated')
        return redirect('profile')

     else:
       u_form = UserUpdateForm(instance=request.user)
       p_form = ProfileUpdateForm(instance=request.user.profile)

     context = {
           'u_form':u_form,
           'p_form':p_form
             }
     return render(request,'users/profile.html',context)
