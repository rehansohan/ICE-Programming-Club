from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Session(models.Model):
    year = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.year


class Member(models.Model):
    POSITION_CHOICES = [
        ('member','Member'),
        ('admin','Admin'),
        ('president','President'),
        ('vice_president','Vice President'),
        ('secretary','Secretary'),
    ]

    STATUS_CHOICES = [
        ('active','Active'),
        ('alumni','Alumni'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100, unique=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='member')
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png')
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)
    codeforces_handle = models.CharField(max_length=100, blank=True)
    codechef_handle = models.CharField(max_length=100, blank=True)
    atcoder_handle = models.CharField(max_length=100, blank=True)

    cf_rating = models.IntegerField(default=0)
    cc_rating = models.IntegerField(default=0)
    at_rating = models.IntegerField(default=0)
    
    @property
    def name(self):
        # Try common CustomUser fields safely
        if hasattr(self.user, "full_name") and self.user.full_name:
            return self.user.full_name

        if hasattr(self.user, "username") and self.user.username:
            return self.user.username

        if hasattr(self.user, "email") and self.user.email:
            return self.user.email.split("@")[0]

        return "Unknown"

    def __str__(self):
        return self.user.email
    
    
class JobProfile(models.Model):
    
    JOB_TYPE_CHOICES=[
        ('full_time','Full Time'),
        ('part_time','Part Time'),
        ('internship','Internship'),
        ('remote','Remote'),
        ('contract','Contract'),
    ]
    
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='job_profiles'
    )
    
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    locrtion = models.CharField(max_length=200,blank=True)
    location = models.CharField(max_length=200, blank=True)
  
    
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )
    skills = models.TextField(help_text="coma separated skills")
    
    description = models.TextField(blank = True)
    start_date = models.DateField(blank=True,null=True)
    is_current= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    
    
from django.db import models
from django.contrib.auth import get_user_model

class UserSkill(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_skills'
    )
    skill_name = models.CharField(max_length=100, blank=True)
    
    EXPERIENCE_CHOICES = [
        ('none', 'None'),
        ('6_month', '6 Month/Half Year'),
        ('one_year', '1 Year'),
        ('two_year', '2 Year'),
        ('three_year', '3 Year'),
        ('three_year_plus', '3 Year+'),
    ]
    
    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='none'
    )
    
    description = models.TextField(blank=True)
    
    def __str__(self):
        # user-er username show korbe, na thakle email, then skill + experience
        user_display = getattr(self.user, 'username', str(self.user))
        return f"{user_display} - {self.skill_name} ({self.experience})"



User = get_user_model()
class UserAddress(models.Model):
    ADDRESS_TYPE_CHOICES=[
        ('present','Present Address'),
        ('permanent','Permanent Address'),
    ]
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    address_type= models.CharField(max_length=100,choices=ADDRESS_TYPE_CHOICES)
    street=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=100,blank=True)
    state= models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    postal_code = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return f"{self.user.email}-{self.get_address_type_display()}"

class SiteContent(models.Model):
    #hero Section
        hero_title = models.CharField(max_length=200, default="ICE Programming Club")
        hero_text = models.TextField(default="A community of passionate programmers at NSTU...")
        hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)
        
        
            # About Section
        about_text = models.TextField(default="ICE Programming Club is a student-run community...")
        
           # Mission & Vision
        mission_text = models.TextField(default="To nurture programming talent...")
        vision_text = models.TextField(default="To be the leading programming community at NSTU...")

        def __str__(self):
            return "Site Content"
        class Meta:
          verbose_name = "Site Content"
          verbose_name_plural = "Site Content"
          
          
          
# models.py
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color_class = models.CharField(max_length=30, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class CommunityMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="members")
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='community/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    year = models.PositiveIntegerField(help_text="Year of the membership, e.g., 2026")

    def __str__(self):
        return f"{self.name} ({self.year})"
    
    
    
    
from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    
        
        
        