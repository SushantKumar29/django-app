from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from .tokens import account_activation_token
from .forms import RegisterForm


def login_view(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('/pictures')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(
                    request, 'Account is not verified check your mail.')
                return redirect('/accounts/login')
            login(request, user)
            return redirect('/pictures')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login')
    return render(request, 'accounts/logout.html', {})


def register_view(request):
    form = RegisterForm()
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            to_email = form.cleaned_data.get('email')
            subject = 'Your accounts need to be verified'
            message = f'Hi click the link to verify your account http://{current_site.domain}/activate/{uidb64}/{token}'
            send_mail_after_registration(subject, to_email, message)
            messages.success(
                request, 'Please confirm your email address to complete the registration')
            return redirect('/accounts/login')
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user.is_active:
        messages.success(request, 'Your account is already verified.')
        return redirect('/accounts/login')
    else:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('/accounts/login')
        else:
            return HttpResponse('Activation link is invalid!')


def send_mail_after_registration(subject, email, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def password_reset_view(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Gallery',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER,
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("done/")
    password_reset_form = PasswordResetForm()
    context = {"password_reset_form": password_reset_form}
    return render(request=request, template_name="accounts/password/password_reset.html", context=context)
