import os
from string import Template

from django import forms
from django.conf import settings

from django.forms import ModelForm , inlineformset_factory

from django.utils.safestring import mark_safe

from account.forms import RegistrationForm
from account.models import Account
from .models import MyProfile, Hobbies, MyEdu, MySkills, MyExpreience, MyActivity, MyAddress, City, Iam, Uploda_Resume

import time

class MyProfileForm(forms.ModelForm):
    AVAILABLE = (
        ('For hire', 'hire'),
        ('Professional', 'Professional'),
        ('student', 'Student')
    )

    bio_data='I grew up in Sremska Kamenica,' \
             ' suburban neighborhood of Novi Sad, where I also finished elementary school. ' \
             'As a kid I would spend my time making toys, reading comics,' \
             ' epic fantasy novels and playing video games. During high school,' \
             ' I played guitar in the school orchestra, ' \
             'worked on technical support and special effects for the school theatre and designed bunch of educational animations.' \
             ' During college I started developing small video games as a hobby and began my career as a freelancer utilizing everything I’ve learned through education and on my own.'


    special_activity_data='I’m passionate about technology and developing creative solutions to whichever problem I come across.' \
                     ' I’m an avid reader and music lover.'

    First_name = forms.CharField(max_length=30,  label='First Name' , required=True)
    Last_name = forms.CharField(max_length=30,  label='Last Name')

    email = forms.EmailField(label='Email' , disabled=True)

    contact = forms.IntegerField(label='Contact')

    proforma_image = forms.ImageField(label='Your Proforma Image' , widget=forms.FileInput(attrs={'class': 'form-control inputfile', 'style':'visibility: hidden' , 'disable':'true',}))

    DOB = forms.DateField(required=True , widget=forms.DateInput(attrs={'palceholder':'yyyy/mm/dd'}) )


    bio = forms.CharField(label='Your Biography', required=True ,  widget=forms.Textarea(attrs={'cols':'70', 'rows':'5' ,'placeholder':bio_data ,}))

    special_activity = forms.CharField( max_length=500 , label='Special Activity', widget=forms.Textarea(attrs={'cols':'70','rows':'3' , 'placeholder':special_activity_data}))

    specialist = forms.CharField(max_length=100,  label='Specialist' ,widget=forms.TextInput(attrs={'placeholder':'Web Developer - Designer'}))

    available = forms.ChoiceField( choices=AVAILABLE , label='Available For')

    experience = forms.IntegerField( label='experience')

    class Meta:
        model=MyProfile
        fields=['First_name','Last_name' ,'email' ,'contact'
            ,'proforma_image' ,'DOB' ,'bio' ,'special_activity' ,'specialist', 'available' ,'experience']

    def clean_proforma_image(self):
        print("dj---------")
        if self.initial == {}:
            print("gdgd")
            return self.cleaned_data['proforma_image']
        else:

            if self.cleaned_data['proforma_image'] != self.initial['proforma_image']:
                print(self.cleaned_data['proforma_image'] , 'cleaned data-----')
                print(self.initial['proforma_image'], 'initial data-----')
                if self.initial['proforma_image'] == 'default_proforma/proforma.png':
                    return self.cleaned_data['proforma_image']

                if self.initial['proforma_image'] is not None:
                    try:
                      os.remove(self.initial['proforma_image'].path)
                      # self.initial['proforma_image'].delete()
                    except PermissionError :
                      print("permissionError ----------")
                      return self.cleaned_data['proforma_image']
                    except FileNotFoundError :
                      print("file not found error ----------")
                      return self.cleaned_data['proforma_image']
                    return self.cleaned_data['proforma_image']

                return self.cleaned_data['proforma_image']
            print("not initial value")

        # print(self.initial)
        return self.cleaned_data['proforma_image']





class ProfileHobbies(forms.ModelForm):

    Name=forms.CharField(max_length=30 , required=True, widget=forms.TextInput(attrs={
        'size':'8' , 'palceholder':'fit'
    }))

    Follow=forms.CharField(max_length=30 , required=False, widget=forms.TextInput(attrs={
        'size':'8'
    }))

    class Meta:
        model=Hobbies
        fields = ['Name' , 'Follow']
        exclude = ()




ProfileForm=inlineformset_factory(MyProfile ,Hobbies , form=ProfileHobbies, extra=1 , can_delete=True )






class MyEduForm(forms.ModelForm):
    board_class=forms.CharField(max_length=30 , label='CLASS', widget=forms.TextInput(attrs={'placeholder':'BTECH-IT' ,'size':'15' }))
    board_name=forms.CharField(max_length=30 , label='BOARD/UNIVERSITY',widget=forms.TextInput(attrs={'placeholder':'MAKAUT' ,'size':'15' }))
    year=forms.IntegerField(label='YEAR PASSING',widget=forms.NumberInput(attrs={'placeholder':'2020','maxlength':'4'
      ,'oninput':'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);','style':'width: 13em' }))
    percentage=forms.CharField(max_length=30 , label='DIVISION/PERCENTAGE', widget=forms.TextInput(attrs={'placeholder':'Ist Division/8.04' ,'size':'15'}))
    file=forms.FileField( required=False ,  widget=forms.FileInput(attrs={'class': 'form-control inputfile', 'style':'visibility: hidden' , 'disable':'true',}))

    class Meta:
        model=MyEdu
        fields=['board_class','board_name','year' ,'percentage' , 'file']


    def clean_file(self):
        if self.initial=={}:
         print("gdgd")
         return self.cleaned_data['file']
        else:
            if self.cleaned_data['file'] != self.initial['file']:
                if self.initial['file'] is not None:
                    # self.initial['file'].delete()
                    try:
                        os.remove(self.initial['file'].path)
                        # self.initial['proforma_image'].delete()
                    except PermissionError:
                        return self.cleaned_data['flle']
                    except FileNotFoundError:
                        return self.cleaned_data['file']

                    return self.cleaned_data['file']

                return self.cleaned_data['file']
            print("not initial value")

        print(self.initial)
        return self.cleaned_data['file']

        # if self.cleaned_data['file']:
        #     print(self.cleaned_data['file'])
        #     print(self.initial['file'])

        # if self.cleaned_data['file'] != self.initial['file']:
        #     print(self.cleaned_data['file'])
        #     if self.initial['file'] is not None:
        #         print(self.initial['file'],'initial files--')
        #         self.initial['file'].delete()
        #         return self.cleaned_data['file']

        #  print("dggf-------")
        #  print(self.initial['file'])
        # # self.initial['file'].delete()
        #  file=self.cleaned_data['file']
        #  print(file)
        #  return file

    # def clean_board_class(self):
    #     data=self.cleaned_data['board_class']
    #     if data=='MAKAUT':
    #      raise forms.ValidationError('MAKAUT student is not allow')
    #     return data





    # def save(self, commit=True):
    #     edu = super(MyEduForm, self).save(commit=False)
    #     file_type = self.cleaned_data['file']
    #     print(file_type)
    #     edu.file_type = file_type
    #     # post.activity_type = Activity.DOWN_VOTE
    #     if commit:
    #         edu.file=file_type
    #         edu.save()
    #     return edu

EducationForm=inlineformset_factory(MyProfile , MyEdu , form=MyEduForm , extra=1 , can_delete=True )





class MySkillsForm(forms.ModelForm):
    SkillText='WordPress, HTML, SCSS, gulp.js, JavaScript, jQuery, React.js'
    SkillDependency='Build WordPress themes utilizing Elementor page builder and Gulp.js ' \
                    'in order to implement designs from Figma into a working Elementor website ' \
                    'with great backend UX. Writing mai 	' \
                    'ntainable and scaleable SCSS, handling all interactions using jQuery.'


    skill_name=forms.CharField(max_length=100 , required=False , widget=forms.TextInput(attrs={'placeholder':'Web Developement'}))
    session=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'size':'12','placeholder':'02/14 – 07/15'}) , required=False)
    skill_text=forms.CharField(max_length=500 , widget=forms.Textarea({'cols':'25', 'rows':'2' ,'placeholder':SkillDependency}) , required=False)
    skill_dependency=forms.CharField(max_length=500, widget=forms.Textarea({'cols': '25', 'rows': '2' , 'placeholder':SkillText}) , required=False)
    class Meta:
        model=MySkills
        fields=['session','skill_name' , 'skill_dependency' , 'skill_text']

SkillsForm=inlineformset_factory(MyProfile , MySkills , form=MySkillsForm , extra=1 , can_delete=True)



class MyExpreienceForm(forms.ModelForm):
    expreience=forms.CharField(max_length=30 , required=True, label='expreience', widget=forms.TextInput(attrs={'placeholder':'02/14 – 07/15'}))
    job_title=forms.CharField(max_length=30 ,required=True, label='Job Title',widget=forms.TextInput(attrs={'placeholder':'web developer'}))
    company_name=forms.CharField(max_length=30 , label='Company Name', widget=forms.TextInput(attrs={'placeholder':'IBM india'}))
    file=forms.FileField( required=False ,  widget=forms.FileInput(attrs={'class': 'form-control inputfile', 'style':'visibility: hidden' , 'disable':'true',}))

    class Meta:
        model=MyExpreience
        fields=['expreience','job_title','company_name' ,'file' ,]

    def clean_file(self):
        if self.initial=={}:
         print("gdgd")
         return self.cleaned_data['file']
        else:
            if self.cleaned_data['file'] != self.initial['file']:
                if self.initial['file'] is not None:
                    # self.initial['file'].delete()
                    try:
                        os.remove(self.initial['file'].path)
                        # self.initial['proforma_image'].delete()
                    except PermissionError:
                        return self.cleaned_data['flle']
                    except FileNotFoundError:
                        return self.cleaned_data['file']

                    return self.cleaned_data['file']

                return self.cleaned_data['file']

            print("not initial value")

        print(self.initial ,'initial file---')
        print(self.cleaned_data['file'])
        # self.initial['file'].delete()
        return self.cleaned_data['file']

ExpreienceForm=inlineformset_factory(MyProfile , MyExpreience , form=MyExpreienceForm , extra=1 , can_delete=True )


class MyActivityForm(forms.ModelForm):
    activity_name=forms.CharField(label='Activity' , required=False , widget=forms.TextInput(attrs={'class': 'form-control'}))
    activity_url=forms.URLField(label='URL' , required=False , widget=forms.URLInput(attrs={'class': 'form-control'}))
    activity_head_image=forms.ImageField(label='Head Image' , required=False, widget=forms.FileInput(attrs={'class': 'form-control inputfile', 'style':'visibility: hidden' , 'disable':'true',}))
    activity_head_report=forms.FileField(label='Report' , required=False , widget=forms.FileInput(attrs={'class':'form-control inputfile','style':'visibility:hidden','disable':'true'}))

    class Meta:
        model=MyActivity
        fields=['activity_name', 'activity_url','activity_head_image' ,'activity_head_report']

    def clean_activity_head_image(self):
        if self.initial=={}:
         print("gdgd")
         return self.cleaned_data['activity_head_image']
        else:
            if self.cleaned_data['activity_head_image'] != self.initial['activity_head_image']:
                if self.initial['activity_head_image'] is not None:
                    try:
                        os.remove(self.initial['activity_head_image'].path)
                        # self.initial['proforma_image'].delete()
                    except PermissionError:
                        return self.cleaned_data['activity_head_image']
                    except FileNotFoundError:
                        return self.cleaned_data['activity_head_image']

                    return self.cleaned_data['activity_head_image']

                return self.cleaned_data['activity_head_image']
            print("not initial value")

        print(self.initial ,'initial file---')
        print(self.cleaned_data['activity_head_image'])
        # self.initial['file'].delete()
        return self.cleaned_data['activity_head_image']

    def clean_activity_head_report(self):
        '''this method is called when we can't pass any file'''
        if self.initial == {}:
            print(self.cleaned_data['activity_head_report'] , '--------')
            return self.cleaned_data['activity_head_report']
        else:
            if self.cleaned_data['activity_head_report'] != self.initial['activity_head_report']:
                print("clean data report is  -------")
                if self.initial['activity_head_report'] is not None:
                        print("initial report is none -------")
                        try:
                            os.remove(self.initial['activity_head_report'].path)
                            # self.initial['proforma_image'].delete()
                        except PermissionError:
                            return self.cleaned_data['activity_head_report']
                        except FileNotFoundError:
                            return self.cleaned_data['activity_head_report']

                        return self.cleaned_data['activity_head_report']
                print("initial report is not none --- -------")
                return self.cleaned_data['activity_head_report']
            print("not initial value")

        print(self.initial, 'initial file---')
        #---------this cleaned_data['activity_head_report'] is complet database file path -------
        print(self.cleaned_data['activity_head_report'])
        # self.initial['file'].delete()
        return self.cleaned_data['activity_head_report']

ActivityForm=inlineformset_factory(MyProfile , MyActivity , form=MyActivityForm , extra=1 , can_delete=True)



class ContactForm(forms.ModelForm):


    email = forms.EmailField(label='Email', disabled=True)
    contact=forms.IntegerField( widget=forms.NumberInput(attrs={}))
    website=forms.URLField(label='Website' , required=False , widget=forms.URLInput(attrs={'class': 'form-control'}))

    postal_code=forms.IntegerField(required=True , widget=forms.NumberInput(attrs={}))




    class Meta:
        model = MyAddress
        fields = ('email', 'contact', 'website', 'country', 'city' , 'postal_code')

    def clean(self):
        data=super(ContactForm , self).clean()
        print(data)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   

        if 'country' in self.data:

            try:
                country_id = int(self.data.get('country'))
                print(country_id)
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):

                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:

            pass
            # self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


# class SendEmail(forms.Form):
#     subject=forms.CharField(max_length=10 , label='subject' , required=True)
#     email=forms.EmailField(max_length=50 ,  label='Email' ,  )
#     body=forms.CharField( required=True, widget=forms.Textarea(attrs={'rows':'5' , 'cols':'5'}) , label='message')
#
#     def clean_email(self):
#         print(self.initial)
#         return self.cleaned_data['email']
#         # if not self['email'].html_name in self.data:
#         #     return self.fields['email'].initial
#         # return self.cleaned_data['email']
#
#     def __init__(self ,user_id , *args , **kwargs):
#         super(SendEmail , self).__init__(*args , **kwargs)
#         print(user_id)
#
#         if user_id is not None:
#          account = Account.objects.get(id=user_id)
#          email=account.email
#          # self.fields['email'].initial=email
#          # self.fields['email'].widget.attrs['value']=email


class SendEmail(forms.Form):
    subject=forms.CharField(max_length=10 , label='subject' , required=True)
    email=forms.EmailField(max_length=50 ,  label='Email' ,  )
    body=forms.CharField( required=True, widget=forms.Textarea(attrs={'rows':'5' , 'cols':'5'}) , label='message')

    # def clean_email(self):
    #     print(self.initial)
    #     return self.cleaned_data['email']
    #     # if not self['email'].html_name in self.data:
    #     #     return self.fields['email'].initial
    #     # return self.cleaned_data['email']
    #
    # def __init__(self , *args , **kwargs):
    #     super(SendEmail , self).__init__(*args , **kwargs)


class IAm(forms.ModelForm):

    iam=forms.CharField(max_length=50 , required=False , label='I AM' , widget=forms.TextInput(attrs={'size':50}))

    class Meta:
        model=Iam
        fields=['iam' , ]

IAmForm=inlineformset_factory(MyProfile , Iam , form=IAm , extra=1 , can_delete=True )


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Uploda_Resume
        fields = ('file', )