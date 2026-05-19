from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import CustomUser, Member, Session,UserAddress,JobProfile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    student_id = forms.CharField(max_length=100, required=True)
    session = forms.ModelChoiceField(queryset=Session.objects.none(), required=True)
    gender = forms.ChoiceField(
    choices=CustomUser.GENDER_CHOICES,
    required=True,
    widget=forms.Select(attrs={'class': 'input-field'})
)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].queryset = Session.objects.all()

    # ✅ Email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # 🔥 THIS FIXES YOUR CURRENT ERROR
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Member.objects.filter(student_id=student_id).exists():
            raise ValidationError("This student ID is already registered.")
        return student_id

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.gender = self.cleaned_data['gender']

        if commit:
            user.save()

            Member.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                session=self.cleaned_data['session'],
                department='ICE'
            )

        return user
    
    
from django import forms
from.models import UserSkill

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields =['skill_name','experience','description']
        

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address_type','street','city','state','country','postal_code']
        
        


class JobPforfileForm(forms.ModelForm):
    class Meta:
        model = JobProfile
        fields=[
            'job_title','company_name','location','job_type','skills','description','start_date','is_current'
        ]
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'description':forms.Textarea(attrs={'row':4}),
        }


from django import forms
from .models import SiteContent

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        fields = "__all__"
        widgets = {
            "hero_title": forms.TextInput(attrs={"class": "form-control"}),
            "hero_text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "about_text": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "mission_text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "vision_text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
        
from.models import CommunityMember

class CommunityMemberForm(forms.ModelForm):
    class Meta:
        model = CommunityMember
        fields =['name','role','image','linkedin','email','year']
        widgets={
            'bio':forms.Textarea(attrs ={'rows':3}),
            'year':forms.NumberInput(attrs={'min':2000,'max':2100}),
        }
        
        
from django import forms
from .models import Member

class MemberHandleForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'codeforces_handle',
            'codechef_handle',
         
            'atcoder_handle'
        ]
        widgets = {
            'codeforces_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Codeforces handle'
            }),
            'codechef_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CodeChef handle'
            }),
    
            'atcoder_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'AtCoder handle'
            }),
        }
        
        
        
        
from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notice title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notice description', 'rows': 4}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
        
from django import forms
from .models import Session

class MemberFilterForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        required=False,
        empty_label="All Sessions",
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    
    
from django import forms
from .models import Member

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['profile_picture']
        
        
        

from django import forms
from .models import CustomUser, Member, JobProfile, UserSkill, UserAddress


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'gender', 'birthday']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user']

class JobProfileForm(forms.ModelForm):
    class Meta:
        model = JobProfile
        exclude = ['user']

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        exclude = ['user']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ['user']

