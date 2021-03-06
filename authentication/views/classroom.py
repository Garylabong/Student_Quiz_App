from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from authentication.forms import EditProfileForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from authentication.forms import PasswordChangingForm

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:T_dashboard')
        else:
            return redirect('students:S_dashboard')
    return render(request, 'home.html')

#account activation using gmail account
def success(request):
    return render(request , 'registration/success.html')


def token_send(request):
    return render(request , 'registration/token_send.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/success')

def error_page(request):
    return  render(request , 'registration/error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Click HERE to verify your account! http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangingForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			messages.success(request,('You Have Edited Your Password...'))
			return redirect('home')
	else:
		form = PasswordChangingForm(user= request.user)

	context = {'form': form}
	return render(request, 'registration/change_password.html', context)

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request,('You Have Edited Your Profile...'))
			return redirect('home')
	else:
		form = EditProfileForm(instance= request.user)

	context = {'form': form}
	return render(request, 'registration/edit_profile.html', context)