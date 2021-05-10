import uuid
from smtplib import SMTPAuthenticationError
from urllib.request import parse_keqv_list

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.views.generic.base import View

from account.models import Account
from .forms import MyProfileForm, ProfileForm, EducationForm, SkillsForm, ExpreienceForm, MyActivityForm, ActivityForm, \
    ContactForm, SendEmail, IAmForm, ResumeForm
# Create your views here.
from .models import MyProfile, MyEdu, MyActivity, City, MyAddress, Uploda_Resume
from django.db import transaction

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.core.mail import EmailMultiAlternatives


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def user_profile_home(request):
    return render(request , 'user-home.html')


class UserProfileHome(ListView):
    template_name = 'user-home.html'
    model = Account

    def dispatch(self, request, *args, **kwargs):
        self.user_id=kwargs.get('user_id')
        self.user = Account.objects.get(id=self.user_id)
        return super(UserProfileHome , self).dispatch(request, *args, **kwargs)

    def get_context_data(self,  **kwargs):
        context=super(UserProfileHome , self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            if self.user==self.request.user:
                context['user_id'] = self.user_id
                context['flag'] = 1
                context['profile_image']=self.user.profile_image.url
                print('edit profile')
            else:

                context['flag']=0
                context['user_id'] = self.user_id
                context['profile_image'] = self.user.profile_image.url


        else:
            if self.user_id is not None:
                context['flag']=0
                context['user_id']=self.user_id
                context['profile_image'] = self.user.profile_image.url


        return context



# @cache_page(CACHE_TTL)
def user_about(request):
    id=request.GET.get('id')
    print(id)
    context={}
    if request.method=='GET' and request.is_ajax:
        account = Account.objects.get(id=id)
        friend=Account.objects.exclude(id=id).count()
        profile = account.profile
        hobbies=profile.user_hobbies.all()
        project=profile.my_activity.count()

        context['project'] = project
        context['profile'] = profile
        context['hobbies'] = hobbies
        context['friend'] = friend
        return render(request,'snippest/user-about.html' , context)

@cache_page(CACHE_TTL)
def user_education(request):
    id=request.GET.get('id')
    context={}
    if request.method=='GET' and request.is_ajax:
        account = Account.objects.get(id=id)
        profile = account.profile
        education=profile.my_edu.all()
        context['profile'] = profile
        context['education'] = education
        return render(request,'snippest/user-education.html' , context)

@cache_page(CACHE_TTL)
def user_expreience(request):
    id=request.GET.get('id')
    context={}
    if request.method=='GET' and request.is_ajax:
        account = Account.objects.get(id=id)
        profile = account.profile
        skills = profile.myskills.all()
        context['skills'] = skills
        expreience=profile.my_exp.all()
        context['expreience']=expreience
        return render(request,'snippest/user-expreience.html' , context)

@cache_page(CACHE_TTL)
def user_portfolio(request):
    id=request.GET.get('id')
    context={}
    if request.method == 'GET' and request.is_ajax:
        account = Account.objects.get(id=id)
        profile = account.profile
        activity=profile.my_activity.all()
        context['activity']=activity
        return render(request , 'snippest/user-portfolio.html' , context)

def Git_Link(request):
    id =request.GET.get('id')
    return render(request, 'snippest/user-education.html')

@cache_page(CACHE_TTL)
def user_contact_info(request):
    id=request.GET.get('id')
    context={}
    if request.method=='GET' and request.is_ajax():
        form = SendEmail()
        context['form']=form
        account = Account.objects.get(id=id)
        email = account.email
        context['email']=email
        proforma=account.profile
        address=MyAddress.objects.get(profile=proforma)
        context['address']=address
        return render(request, 'snippest/user-contact.html', context)


def send_email(request):

    if request.is_ajax and request.method == "POST":

        form = SendEmail( request.POST )

        if form.is_valid():
          subject = form.cleaned_data['subject']
          message = form.cleaned_data['body']
          to_email=form.cleaned_data['email']
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




def base_edit(request):
    return render(request , 'base-edit.html')

class download_resume(View):

    # def dispatch(self, request, *args, **kwargs):
    #     id = kwargs.get('user_id')
    #     self.user_id = id
    #     print(id ,'----')
    #     user = Account.objects.get(id=id)
    #     if self.request.user == user:
    #         return super(download_resume, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('accounts:signup')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        return get_object_or_404(MyProfile, id=account.profile.id)

    def get(self, request , *args , **kwargs):
        user_id=kwargs.get('user_id')
        if (Uploda_Resume.objects.filter(profile=self.get_object()).exists()):
            Resume_list = Uploda_Resume.objects.get(profile=self.get_object())
            return render(self.request, 'resume/drag_and_drop_upload/index.html',  {'user_id': user_id, 'Resumes': Resume_list})
        else:
         return render(self.request, 'resume/drag_and_drop_upload/index.html' , {'user_id':user_id , 'Resumes':None})

    def post(self, request , *args , **kwargs):
        Resume_FILE_TYPES = ['png', 'jpg', 'jpeg', 'pdf', 'doc' ]
        user_id = kwargs.get('user_id')
        form = ResumeForm(self.request.POST, self.request.FILES)
        data = request.POST.get('var')
        print(data)
        if form.is_valid():

            print(request.FILES)
            document = form.save(commit=False)
            file_typr = document.file.url.split('.')[-1]
            file_typr = file_typr.lower()
            if file_typr not  in Resume_FILE_TYPES:
                return JsonResponse({'error':'invalid_file_type'} , status=400)
            account = Account.objects.get(id=user_id)
            myprofile = account.profile
            if( Uploda_Resume.objects.filter(profile=myprofile).exists()):
                object=Uploda_Resume.objects.get(profile=myprofile)
                object.file.delete()
                object.delete()
                document.profile = myprofile
                document.save()
                data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url}
                print(True)
            else:
                document.profile=myprofile
                document.save()
                data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url}
        else:
            jsonD = json.dumps(form.errors)
            data = {'is_valid': False}
            return JsonResponse({'error': jsonD}, status=400)
        return JsonResponse(data)

def edit_user_about(request , user_id):
    account = Account.objects.get(id=user_id)
    myprofile = account.profile
    print(myprofile.id)
    if request.method=='GET':
        form=MyProfileForm(instance=myprofile)
        return render(request , 'edit-activity/my-profile.html' , {'form':form})
    if request.method=='POST':
        form=MyProfileForm(request.POST, request.FILES , instance=myprofile )
        if form.is_valid():
            form.save()
            return redirect('user-profile:user-home')

        return render(request, 'edit-activity/my-profile.html', {'form': form})


#
class MyProfileUpdate(UpdateView):
    template_name = 'edit-activity/my-profile.html'
    model = MyProfile
    form_class = MyProfileForm
    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        return get_object_or_404(MyProfile, id=account.profile.id)

    def dispatch(self, request, *args, **kwargs):
        id=kwargs.get('user_id')
        self.user_id=id
        user=Account.objects.get(id=id)
        if self.request.user==user:
         return super(MyProfileUpdate , self).dispatch(  request , *args , **kwargs)
        else:
            return redirect('accounts:signup')


    def get_context_data(self, **kwargs):
        data = super(MyProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['profile_hobbies'] = ProfileForm(self.request.POST , instance=self.object)
        else:
            print(self.object)
            data['profile_hobbies'] = ProfileForm(instance=self.object)
        return data




    def form_valid(self, form):
            print("2------")
            context = self.get_context_data()
            # print(context)
            profile_hobbies = context['profile_hobbies']

            with transaction.atomic():
                print('befour save------')
                self.object = form.save()
                if profile_hobbies.is_valid():
                    profile_hobbies.instance = self.object
                    print('after save------')
                    profile_hobbies.save()
                else:
                    return render(self.request , 'edit-activity/my-profile.html',{'form': MyProfileForm(self.request.POST, instance=self.object),'profile_hobbies': ProfileForm(self.request.POST , instance=self.object)})

            return super( MyProfileUpdate, self).form_valid(form)
            # return redirect('profile-list')

    def get_success_url(self):
        return reverse_lazy('user-profile:edit-user-edication', kwargs={'user_id': self.user_id})
        # return reverse_lazy('user-profile:edit-profile-home', kwargs={'user_id': self.user_id})


# class MyEducation(UpdateView):
#     template_name = 'edit-activity/my-education.html'
#     model = MyProfile
#     form_class = MyProfileForm
#
#     def get_object(self, queryset=None):
#         id_ = self.kwargs.get("user_id")
#         account = Account.objects.get(id=id_)
#         return get_object_or_404(MyProfile, id=account.profile.id)
#
#     def dispatch(self, request, *args, **kwargs):
#         id = kwargs.get('user_id')
#         print(id)
#         user = Account.objects.get(id=id)
#         if self.request.user == user:
#             return super(MyEducation, self).dispatch(request, *args, **kwargs)
#         else:
#             return redirect('accounts:signup')
#
#     def get_context_data(self, **kwargs):
#         data = super(MyEducation, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['profile_education'] = EducationForm(self.request.POST, instance=self.object)
#         else:
#             data['profile_education'] = EducationForm(instance=self.object ,)
#         return data
#
#     def form_valid(self, form):
#         print("hjgd----------")
#         context = self.get_context_data()
#         # print(context)
#         profile_education = context['profile_education']
#
#         with transaction.atomic():
#             self.object = form.save()
#             if profile_education.is_valid():
#                 profile_education.instance = self.object
#                 profile_education.save()
#             else:
#
#                 return render(self.request, 'edit-activity/my-education.html',
#                               {'form': MyProfileForm(self.request.POST, instance=self.object),
#                                'profile_hobbies': EducationForm(self.request.POST, instance=self.object)})
#
#         return super(MyEducation, self).form_valid(form)
#         # return redirect('profile-list')
#
#     def get_success_url(self):
#         return reverse_lazy('user-profile:user-home')


class MyEducation(UpdateView):
    template_name = 'edit-activity/my-education.html'
    form_class = MyProfileForm
    # model = MyProfile

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        return get_object_or_404(MyProfile, id=account.profile.id)

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('user_id')
        print(id)
        self.user_id=id
        user = Account.objects.get(id=id)
        if self.request.user == user:
            return super(MyEducation, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:signup')

    def get_context_data(self,  **kwargs):
        data = super(MyEducation, self).get_context_data(**kwargs)
        if self.request.POST:
            data['profile_education'] = EducationForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            print(self.object)
            data['profile_education'] = EducationForm(instance=self.object)
            data['profile']=self.object
        return data

    def post(self, request, *args, **kwargs):
        super(MyEducation , self).post(request , *args ,**kwargs)
        context = self.get_context_data()
        profile_education = context['profile_education']

        with transaction.atomic():

            if profile_education.is_valid():
                profile_education.instance = self.object
                profile_education.save()
                # return redirect('user-profile:user-home')

                return  redirect( reverse_lazy('user-profile:edit-user-skills', kwargs={'user_id': self.user_id}))
            else:
                print(profile_education.errors)
                return render(request, 'edit-activity/my-education.html', {'profile_education':context['profile_education'] ,
                                                                           'profile':self.object} )


class I_AM(UpdateView):
    template_name = 'edit-activity/I-am.html'
    form_class = MyProfileForm

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        print(get_object_or_404(MyProfile, id=account.profile.id) , '-----------')
        return get_object_or_404(MyProfile, id=account.profile.id)

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('user_id')
        print(id)
        self.user_id = id
        user = Account.objects.get(id=id)
        if self.request.user == user:
            return super(I_AM, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:signup')

    def get_context_data(self,  **kwargs):
        data = super(I_AM, self).get_context_data(**kwargs)
        if self.request.POST:
            data['I_AM'] = IAmForm(self.request.POST, instance=self.object)
        else:
            print(self.object)
            data['I_AM'] = IAmForm(instance=self.object)
            data['profile']=self.object
        return data

    def post(self, request, *args, **kwargs):
        super(I_AM, self).post(request, *args, **kwargs)
        context = self.get_context_data()
        iam = context['I_AM']

        with transaction.atomic():

            if iam.is_valid():
                iam.instance = self.object
                iam.save()
                # return redirect('user-profile:user-home')

                return redirect(reverse_lazy('user-profile:edit-user-activity', kwargs={'user_id': self.user_id}))
            else:
                print(iam.errors)
                return render(request, 'edit-activity/I-am.html',
                              {'I_AM': context['I_AM'],
                               'profile': self.object})



    # def form_valid(self, form):
    #     print("hjgd----------")
    #     context = self.get_context_data()
    #     # print(context)
    #     profile_education = context['profile_education']
    #
    #     with transaction.atomic():
    #         self.object = form.save()
    #         if profile_education.is_valid():
    #             profile_education.instance = self.object
    #             profile_education.save()
    #         else:
    #
    #             return render(self.request, 'edit-activity/my-education.html',
    #                           {'form': MyProfileForm(self.request.POST, instance=self.object),
    #                            'profile_hobbies': EducationForm(self.request.POST, instance=self.object)})
    #
    #     return super(MyEducation, self).form_valid(form)
        # return redirect('profile-list')

    def get_success_url(self):
        return reverse_lazy('user-profile:user-home')


def profile_education(request , user_id):
    account = Account.objects.get(id=user_id)
    profile_instance=get_object_or_404(MyProfile, id=account.profile.id)
    print(profile_instance)
    if request.method=='GET':
        print("fhfh---")
        profile_education=EducationForm(instance=profile_instance)
        return render(request, 'edit-activity/my-education.html',{'profile_education':profile_education})

    if request.method=='POST':
        profile_education = EducationForm(request.POST , request.FILES, instance=profile_instance)

        with transaction.atomic():

            if profile_education.is_valid():

                for file  in request.FILES:

                    print(file)
                    print(file[7:8])
                    id=file[7:8]
                    image=MyEdu.objects.filter()
                    print(image)
                    # image.delete()


                    # print(request.FILES['file'].all())
                    # for edu_object in profile_instance.my_edu.all():
                    #     print(edu_object.file)
                    # print(profile_instance.my_edu.all())
                    # file = request.FILES['file']
                    # handle_uploaded_file(request.FILES['file'])

                # print(profile_education.cleaned_data)

                profile_education.instance=profile_instance
                profile_education.save()
                print("is_valid")
                return redirect('user-profile:user-home')
            else:
                return render(request, 'edit-activity/my-education.html', {'profile_education': profile_education})

    # return  render(request, 'edit-activity/my-education.html', {'profile_education': profile_education})


def handle_uploaded_file(f):
    print(f)
    with open('media/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
          destination.write(chunk)





class MySkill(UpdateView):
    template_name = 'edit-activity/my-skills.html'
    form_class = MyProfileForm
    # model = MyProfile

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        return get_object_or_404(MyProfile, id=account.profile.id)

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('user_id')
        self.user_id=id
        print(id)
        user = Account.objects.get(id=id)
        if self.request.user == user:
            return super(MySkill, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:signup')

    def get_context_data(self,  **kwargs):
        data = super(MySkill, self).get_context_data(**kwargs)
        if self.request.POST:
            data['skills'] = SkillsForm(self.request.POST, self.request.FILES, instance=self.object)
            data['expreience'] = ExpreienceForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            print(self.object)
            data['skills'] = SkillsForm(instance=self.object)
            data['expreience'] = ExpreienceForm(instance=self.object)

        return data

    def post(self, request, *args, **kwargs):
        super(MySkill , self).post(request , *args ,**kwargs)
        context = self.get_context_data()
        skills = context['skills']
        expreience = context['expreience']

        with transaction.atomic():

            if skills.is_valid() and expreience.is_valid():
                skills.instance = self.object
                expreience.instance = self.object
                skills.save()
                expreience.save()
                return redirect(reverse_lazy('user-profile:I-am', kwargs={'user_id': self.user_id}))
                # return redirect('user-profile:user-home')
            else:
                print(expreience.errors)

                return render(request, 'edit-activity/my-skills.html', {'skills': context['skills'],
                                                                        'expreience': expreience})

            # if expreience.is_valid():
            #     expreience.instance = self.object
            #     expreience.save()
            #     return redirect('user-profile:user-home')
            # else:
            #     print(expreience.errors)
            #     return render(request, 'edit-activity/my-skills.html', {'skills': context['skills'],
            #                                                             'expreience': expreience})






# class MySkill(UpdateView):
#     template_name = 'edit-activity/my-skills.html'
#     form_class = MyProfileForm
#     # model = MyProfile
#
#     def get_object(self, queryset=None):
#         id_ = self.kwargs.get("user_id")
#         account = Account.objects.get(id=id_)
#         return get_object_or_404(MyProfile, id=account.profile.id)
#
#     def dispatch(self, request, *args, **kwargs):
#         id = kwargs.get('user_id')
#         print(id)
#         user = Account.objects.get(id=id)
#         if self.request.user == user:
#             return super(MySkill, self).dispatch(request, *args, **kwargs)
#         else:
#             return redirect('accounts:signup')
#
#     def get_context_data(self,  **kwargs):
#         data = super(MySkill, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['skills'] = SkillsForm(self.request.POST, self.request.FILES, instance=self.object)
#             data['expreience'] = ExpreienceForm(self.request.POST, self.request.FILES, instance=self.object)
#         else:
#             print(self.object)
#             data['skills'] = SkillsForm(instance=self.object)
#             data['expreience'] = ExpreienceForm(instance=self.object)
#
#         return data
#
#     def post(self, request, *args, **kwargs):
#         super(MySkill , self).post(request , *args ,**kwargs)
#         context = self.get_context_data()
#         skills = context['skills']
#         expreience = context['expreience']
#
#         with transaction.atomic():
#
#             if skills.is_valid():
#                 skills.instance = self.object
#                 skills.save()
#                 return redirect('user-profile:user-home')
#             else:
#                 print(skills.errors)
#                 return render(request, 'edit-activity/my-skills.html', {'skills':context['skills'] ,
#                                                                          'expreience': expreience} )
#
#             if expreience.is_valid():
#                 expreience.instance = self.object
#                 expreience.save()
#                 return redirect('user-profile:user-home')
#             else:
#                 print(expreience.errors)
#                 return render(request, 'edit-activity/my-skills.html', {'skills': context['skills'],
#                                                                         'expreience': expreience})

from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json

def my_activity(request , user_id):
    account=Account.objects.get(pk=user_id)
    profile=account.profile

    if request.is_ajax and request.method == "POST":
        # get the form data

        form = MyActivityForm(request.POST , request.FILES)
        # save the data and after fetch the object in instance
        if form.is_valid():

            instance = form.save(commit=False)
            instance.profile=profile
            instance.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            # converts the raw HTML content into a JSON string representation. jsonL = json.loads(jsonD)
            print(form.errors)
            jsonD = json.dumps(form.errors)
            print(jsonD)
            return JsonResponse({"error": jsonD}, status=400)


    activity=profile.my_activity.all()
    print(activity)
    form= MyActivityForm()
    return render(request , 'edit-activity/my-activity.html', {'form':form , 'activity':activity})



from PIL import Image

class MyProtfolio(UpdateView):
    template_name = 'edit-activity/my-activity.html'
    form_class = MyProfileForm
    # model = MyProfile

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        return get_object_or_404(MyProfile, id=account.profile.id)

    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs.get('user_id')
        user = Account.objects.get(id=self.id)
        if self.request.user == user:
            return super(MyProtfolio, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:signup')

    def get_context_data(self,  **kwargs):
        data = super(MyProtfolio, self).get_context_data(**kwargs)
        if self.request.POST:
            data['protfolio'] = ActivityForm(self.request.POST, self.request.FILES, instance=self.object)
        else:
            print(self.object)
            data['protfolio'] = ActivityForm(instance=self.object)
            data['activity']=self.object.my_activity.all()
        return data

    def post(self, request, *args, **kwargs):
        super(MyProtfolio , self).post(request , *args ,**kwargs)
        context = self.get_context_data()
        protfolio = context['protfolio']

        with transaction.atomic():

            if  protfolio.is_valid():
                protfolio.instance = self.object



                # image = Image.open(protfolio.activity_head_image)
                # size = (1080, 1080)
                # image = image.resize(size, Image.ANTIALIAS)
                # image.save(protfolio.activity_head_image.path)

                print("delete method is ----------")
                protfolio.save()
                return redirect(reverse('user-profile:edit-user-activity', kwargs={'user_id': self.id}))
                # return redirect('user-profile:user-home')
            else:
                print(protfolio.errors)
                return render(request, 'edit-activity/my-activity.html', {'protfolio':context['protfolio'] ,
                                                                           'activity':self.object.my_activity.all()} )


class myAddress(UpdateView):
    template_name = 'edit-activity/my-address.html'
    form_class = ContactForm
    model = MyAddress

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("user_id")
        account = Account.objects.get(id=id_)
        profile=get_object_or_404(MyProfile, id=account.profile.id)
        return get_object_or_404(MyAddress , profile=profile)

    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs.get('user_id')
        user = Account.objects.get(id=self.id)
        if self.request.user == user:
            return super(myAddress, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:signup')

    def form_valid(self, form):
        return super(myAddress, self).form_valid(form)


    def get_success_url(self):
        return reverse_lazy('user-profile:edit-profile-home', kwargs={'user_id': self.id})







def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown/city_dropdown_list_options.html', {'cities': cities})
