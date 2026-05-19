from django.contrib import admin
from .models import CustomUser, Session, Member,JobProfile,UserSkill,UserAddress,CommunityMember,Role


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    list_filter = ('is_staff', 'is_active')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department', 'position', 'status', 'is_verified')
    list_filter = ('position', 'status', 'is_verified')
    search_fields = ('student_id', 'user__email', 'department')
    
@admin.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
    list_display=(
        'job_title',
        'company_name',
        'user',
        'job_type',
        'is_current',
        'created_at',
    )
    list_filter=('job_type','is_current')
    search_fields=('job_title','company_name','user__email')
    


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'user', 'experience', 'description')
    list_filter = ('experience', 'user')
    search_fields = ('skill_name', 'description', 'user__username')
    ordering = ('user', 'skill_name')
    
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user','address_type','street','city','state','country','postal_code',)
    list_filter=('address_type','user')
    search_fields=('user__username','street','city','state','country','postal_code')
    ordering =('user','address_type')
    
    
from django.contrib import admin
from .models import SiteContent

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('hero_title',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'color_class')
    list_editable = ('order', 'color_class')

@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    list_filter = ('role',)
    search_fields = ('name',)
    
    
    
from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_pinned')
    list_filter = ('is_pinned',)

    def save_model(self, request, obj, form, change):
        if obj.is_pinned:
            Notice.objects.filter(is_pinned=True).update(is_pinned=False)
        super().save_model(request, obj, form, change)
