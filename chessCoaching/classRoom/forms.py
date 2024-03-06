from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# from django.contrib.auth
from .models import Student
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import re
from django.db import transaction
# from .models import Assignment


class RegisterForm(forms.ModelForm):
    phone = PhoneNumberField(widget =PhoneNumberPrefixWidget(initial='IN',attrs={"class":"special"}))
    date_of_birth=forms.DateField(input_formats=['%d/%m/%Y'],widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}),label="Date Of Birth") #add placeholder dd/mm/yyyy
    confirm_password=forms.CharField(max_length=255,label="Confirm Password")
    academy_interested=forms.TypedChoiceField(choices=Student.academy,widget=forms.Select(attrs={'class': 'special'}),
        coerce=str,label="Academy Interested")

    class Meta:
        model=Student 
        exclude = ['id']
        # fields=("confirm_password","password")
        

    def clean_student_email(self):
        email=self.cleaned_data['student_email'].lower()
        mail,domain=email.split("@")
        if domain in ["hotmail.com","gmail.com","yahoo.com","example.com"]: #remove example.com
            return email
        else:
            raise ValidationError("Provide valid email address")
        
    def clean_bloodgrp(self):
        # print(self.cleaned_data)
        blood=self.cleaned_data['bloodgrp'].upper()
        regex=r"^(A|B|AB|O)[+-]$"
        if re.match(regex,blood):
            return blood
        else:
            raise ValidationError("Provide Blood Grp in form of A+ ,B-")
    
   
    
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        if self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
            if validate_password(self.cleaned_data['password']) == None:
                self.cleaned_data['password']= make_password(self.cleaned_data['confirm_password'])
                print( self.cleaned_data['password'])
                return 
            else:
                raise validate_password(self.cleaned_data['password'])
        else:
            raise ValidationError(" The passwords dont match")
    #send mail based on the admin of the academy teacher for approval

    def save(self):
        instance= super(RegisterForm,self).save()

        @transaction.on_commit
        def sending_email():
            send_mail("Subject here",
                "message",
                "from@example.com",
                [self.cleaned_data["student_email"]],
                fail_silently=False,)
        
        return instance
        
#login form
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,required =True)
    password = forms.CharField(widget=forms.PasswordInput,label="Password")

    # class Meta:
    #     model=Student
    #     fields=['username','password']

    def clean_username(self):
        print("hello")
        if len(self.cleaned_data['username']) > 6 and self.cleaned_data['username'][0:6].upper() == 'CHESS-':
            z=self.cleaned_data['username'][6:]
            print(z,"z")
            return z

        else:
            raise ValidationError(" The username is not valid") 
        
# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignment
#         fields = ['course', 'assignment_name', 'description', 'due_date']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
   
# def clean_confirm_password(self):
#     password = self.cleaned_data.get('password')
#     confirm_password = self.cleaned_data.get('confirm_password')
#     if password and confirm_password:
#         if password == confirm_password:
#             try:
#                 validate_password(password)
#             except ValidationError as e:
#                 raise ValidationError(e)
#             return make_password(password)
#         else:
#             raise ValidationError("The passwords don't match")
#     return confirm_password



    


    
   
        




