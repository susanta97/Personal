from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from account.forms import RegistrationForm, AccountUpdateForm, AccountAuthenticationForm
from account.models import Account
from account.tokens import account_activation_token

from django.conf import settings

from django.core.mail import EmailMessage

from django.contrib.auth import login, authenticate, logout


def register_view(request , *args , **kwargs):
    user=request.user
    if user.is_authenticated:
        return HttpResponse("you are already authenticated as" +str(user.email))
    context={}
    if request.method=="POST" or request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            if settings.RUN_DEVELOPEMENT_SERVER:
                form.save()
                email = form.cleaned_data.get('email').lower()
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect('home:home')

            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('account/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                to_email = form.cleaned_data.get('email')
                email = EmailMessage(subject, message, to=[to_email])
                email.send()
                return redirect('accounts:account_activation_sent')

        else:
            context['registration_form']=form

    else:

        form=RegistrationForm()
        context['registration_form']=form
    return render(request , 'account/singup.html' , context)


def account_activation_sent(request):
    return render(request, 'account/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home:home')
    else:
        return render(request, 'account/account_activation_invalid.html')


def logout_view(request):
    logout(request)
    return redirect("home:home")


def edit_account_view(request, *args, **kwargs):
    print(request.method)
    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
    print(user_id)
    account = Account.objects.get(pk=user_id)
    print(account)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.FILES:
                print(request.FILES)
                if not account.profile_image=="account/blank.png":
                  account.profile_image.delete()

            form.save()
            print("save----")
            new_username = form.cleaned_data['username']
            # return redirect("user-profile:base-edit")
            return redirect(reverse('user-profile:edit-user-about', kwargs={'user_id': user_id}))
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                                     initial={
                                         "id": account.pk,
                                         "email": account.email,
                                         "username": account.username,
                                         "profile_image": account.profile_image,
                                         "hide_email": account.hide_email,
                                     }
                                     )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                "id": account.pk,
                "email": account.email,
                "username": account.username,
                "profile_image": account.profile_image,
                "hide_email": account.hide_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    # return HttpResponse("<h1> hello </h1>")
    return render(request, "account/edit_account.html", context)


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home:home")


    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home:home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "account/login.html", context)