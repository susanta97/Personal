import json
from smtplib import SMTPAuthenticationError

from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect

from account.models import Account
from home.forms import send_email_form
from home.models import  Administrator

import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.views.generic import ListView

from usrprofile.models import MyAddress


class Home(ListView):

    template_name = 'home.html'
    model=Administrator

    def dispatch(self, request, *args, **kwargs):
        user_id=kwargs.get('user_id')
        print(user_id)
        self.user_id=user_id
        return super(Home , self).dispatch( request, *args, **kwargs)

    def get_context_data(self,  **kwargs):
        context=super(Home , self).get_context_data(**kwargs)
        friends=Account.objects.all()

        if self.user_id is not None:
            user=Account.objects.get(id=self.user_id)
            proforma = user.profile
            context['proforma'] = proforma
            expreience = proforma.my_exp.all()
            context['expreience']=expreience

            domain = proforma.iam.all()
            field = []
            for i in domain:
                field.append(i.iam)
            context['domain'] = json.dumps(field)
            context['friends'] = friends

            return context

        if self.request.user.is_authenticated:
            user=self.request.user
            proforma=user.profile
            context['proforma'] = proforma
            expreience = proforma.my_exp.all()
            context['expreience'] = expreience

            domain = proforma.iam.all()
            field = []
            for i in domain:
                field.append(i.iam)
            context['domain'] = json.dumps(field)
            context['friends'] = friends

            return context

        else:
            user=Account.objects.get(username='admin')
            

            proforma = user.profile
            context['proforma']=proforma
            expreience = proforma.my_exp.all()
            context['expreience'] = expreience
            domain = proforma.iam.all()
            field = []
            for i in domain:
                field.append(i.iam)
            context['domain']=json.dumps(field)
            context['friends'] = friends
            return context


def home(request):
    user=Account.objects.get(username='admin')
    pk=user.pk
    print(pk)
    proforma=Administrator.objects.get(user_id=pk)
    domain=proforma.domain.all()
    field=[]
    for i in domain:
        field.append(i.domain)
        print(i.domain)
    return render(request , 'home.html' ,{'proforma':proforma ,'domain':json.dumps(field)})


def  model_login(request):
    payload={}
    if request.is_ajax and request.method == "POST":
        print("gdg")
        username=request.POST.get('username')
        print(username)
        password=request.POST.get('password')
        print(password)
        user = authenticate(email=username, password=password)
        if user:
            print("hfdh--------------")
            login(request, user)
            payload['response'] = "login successfull"
            # return redirect("home")
        else:
         payload['response'] = "user not found"

    return HttpResponse(json.dumps(payload), content_type="application/json")


def download_cv(request , user_id):
    print(user_id ,  '----------')
    context={}

    if user_id is not  None:
        user = Account.objects.get(id=user_id)
        proforma = user.profile
        context['proforma'] = proforma
        expreience = proforma.my_exp.all()
        if len(proforma.my_exp.all()) >= 1:
            print(len(proforma.my_exp.all()))
            context['flag']=1
            context['expreience'] = expreience

        educations=proforma.my_edu.all()

        context['educations'] = educations
        context['skills']=proforma.myskills.all()
        address=MyAddress.objects.get(profile=proforma)
        context['address']=address
        hobbies = proforma.user_hobbies.all()
        context['hobbies']=hobbies

    else:
        pass
    return render(request , 'resume/user_cv.html' , context)

from django.conf import settings

def email_send(request):

    if request.is_ajax and request.method == "POST":

        form = send_email_form( request.POST )

        if form.is_valid():
          subject = form.cleaned_data['subject']
          message = form.cleaned_data['text']
          to_email=form.cleaned_data['email']
          print(form.cleaned_data)
          from_email=settings.EMAIL_HOST_USER
          try:
              msg = EmailMultiAlternatives(subject, message, from_email, [to_email])
              msg.send()
          except SMTPAuthenticationError:

              return JsonResponse({"error": 'SMTPAuthenticationError '}, status=400)


          return JsonResponse({"success": 'successfully send the email to '+(form.cleaned_data['email'])+''}, status=200)

        else:
            # some form errors occured.
            # converts the raw HTML content into a JSON string representation. jsonL = json.loads(jsonD)
            print(form.errors)
            jsonD = json.dumps(form.errors)
            print(jsonD)
            return JsonResponse({"error": jsonD}, status=400)