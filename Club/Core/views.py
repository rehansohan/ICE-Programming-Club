from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm,UserSkillForm,UserAddressForm,JobPforfileForm
from.models import JobProfile,UserSkill,UserAddress,Notice


def index(request):
    return render(request, "Core_templates/index.html")

def learning(request):
    return render(request,'public/learning.html')

def blogs(request):
    return render(request,'public/blogs.html')




def home(request):
    content = SiteContent.objects.first()
    pinned_notice = Notice.objects.filter(is_pinned=True).first()
    notices = Notice.objects.filter(is_pinned=False).order_by('-date')

    
    # only single hero image
    hero_images = [content.hero_image] if content and content.hero_image else []
    
    context = {
        'content': content,
        'hero_images': hero_images,
        'pinned_notice': pinned_notice,
        'notices': notices,
    }
    return render(request, 'Core_templates/home.html', context)

def community_members(request):
    return render(request, "public/community_members.html")

def navbar(request):
    return render(request,'navbar.html')


def faculty_members(request):
    return render(request, "public/faculty_members.html")


def about(request):
    return render(request, "Core_templates/about.html")


def alumina(request):
    return render(request, "Core_templates/alumina.html")

def deshboard(request):
    return render(request, "deshboard/deshboard.html")


# ================= REGISTER =================
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()

    return render(request, "Core_templates/register.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")  # must match path name
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "Core_templates/login_page.html")



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')





from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    members = Member.objects.select_related('user', 'session')

    context = {
        'members': members,
        'total_users': User.objects.count(),
        'active_members': members.filter(status='active').count(),
        'alumni_count': members.filter(status='alumni').count(),
        'total_skills': sum(
            len(m.skills.split(',')) if m.skills else 0
            for m in members
        )
    }

    return render(request, "Core_templates/admin_page.html", context)

from .models import Member, Session
def user_list(request):
    session_id = request.GET.get('session')
    members=Member.objects.select_related('user','session')
    
    if session_id:
        members = members.filter(session_id=session_id)
        
    sessions = Session.objects.all()
    
    context ={
        'members':members,
        'sessions':sessions
    }
    
    return render(request,"Core_templates/user.html",context)


def profile_index(request):
     return render(request, "profile/profile_index.html")
 
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Member
from .forms import ProfilePictureForm

@login_required
def personal_information(request):
    member, created = Member.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('personal_information')
    else:
        form = ProfilePictureForm(instance=member)

    context = {
        "member": member,
        "form": form,
    }
    return render(request, "profile/personal_information.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Member, Session

@login_required
def edit_personal_information(request, user_id=None):
    """
    - Normal user edits own info (user_id=None)
    - Admin edits any user (user_id provided)
    """
    # Determine which member to edit
    if user_id:
        # Admin editing another user
        if not request.user.is_staff:
            messages.error(request, "You are not authorized to edit this user.")
            return redirect("personal_information")
        member = get_object_or_404(Member, user__id=user_id)
    else:
        # Normal user editing self
        member, created = Member.objects.get_or_create(
            user=request.user,
            defaults={"student_id": "N/A", "department": "N/A", "session": Session.objects.first()}
        )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        department = request.POST.get("department", "").strip()
        session_id = request.POST.get("session")

        # Validate required fields
        if not name or not email:
            messages.error(request, "Name and email cannot be empty.")
        else:
            try:
                # Update user fields
                member.user.name = name
                member.user.email = email
                member.user.save()

                # Update member fields
                if department:
                    member.department = department
                if session_id:
                    member.session = get_object_or_404(Session, id=session_id)

                member.save()
                messages.success(request, "Profile updated successfully!")

                # Redirect depending on user/admin
                if request.user.is_staff and user_id:
                    return redirect("admin_dashboard")
                return redirect("personal_information")

            except IntegrityError as e:
                messages.error(request, f"Database error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")

    context = {
        "member": member,
        "sessions": Session.objects.all(),  # For session dropdown
    }
    return render(request, "profile/edit_personal_information.html", context)


@login_required
def skill_add(request):
    if request.method =='POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('show_skill')
        
    else :
        form = UserSkillForm()
    
    return render(request,'profile/add_skill.html',{'form':form})

@login_required
def skill_list(request):
    skills=UserSkill.objects.filter(user=request.user)
    return render(request,'profile/skill_profile.html',{'skills':skills})

@login_required
def skill_edit(request,pk):
    skill = get_object_or_404(UserSkill,pk=pk,user=request.user)
    if request.method =='POST':
        form = UserSkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            return redirect('show_skill')
    else :
        form = UserSkillForm(instance=skill)
        
    return render(request,'profile/skill_edit.html',{'form':form})



@login_required
def address_add(request):
    if request.method =='POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            address.user=request.user
            address.save()
            return redirect('address_list')
    else:
        form=UserAddressForm()
    return render(request,'profile/address_edit_add.html',{'form':form})


@login_required
def address_edit(request,pk):
    address = get_object_or_404(UserAddress,pk=pk,user=request.user)
    if request.method =='POST':
        form = UserAddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
        
    else :
        form = UserAddressForm(instance=address)
    return render(request,'profile/address_edit_add.html',{'form':form})
        
            
@login_required
def address_list(request):
    addresses = UserAddress.objects.filter(user=request.user)
    return render(request,'profile/address_form.html',{'addresses':addresses})



@login_required

def job_list(request):
    jobs = JobProfile.objects.filter(user=request.user).order_by('-start_date')
    return render(request,'profile/job_profile.html',{'jobs':jobs})

@login_required
def job_add(request):
    if request.method =='POST':
        form = JobPforfileForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobPforfileForm()
    return render (request,'profile/job_edit_add.html',{'form':form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobProfile


@login_required
def job_edit(request, pk):
    # get the job profile for the logged-in user
    job = get_object_or_404(JobProfile, pk=pk, user=request.user)

    if request.method == 'POST':
        form = JobPforfileForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # redirect instead of render
    else:
        form = JobPforfileForm(instance=job)

    return render(request, 'profile/job_edit_add.html', {'form': form})


from django.shortcuts import render
from .models import Member, JobProfile

def proud_professionals(request):
    """
    Show all members who have a current job.
    One user = one card = current job only
    """
    # Get all current jobs
    current_jobs = JobProfile.objects.filter(is_current=True).select_related('user')

    # Get members who have a current job
    members = Member.objects.filter(user__job_profiles__in=current_jobs).select_related('user', 'session').distinct()

    # Prepare a dictionary mapping member -> current job
    member_jobs = {}
    for member in members:
        current_job = member.user.job_profiles.filter(is_current=True).first()
        if current_job:
            member_jobs[member] = current_job

    return render(request, 'public/proud_professionals.html', {
        'member_jobs': member_jobs
    })
    
from .models import SiteContent
from .forms import SiteContentForm    
    
@login_required
def admin_main_page(request):
    # Ensure only ONE row exists (CMS style)
    content, created = SiteContent.objects.get_or_create(id=1)

    if request.method == "POST":
        form = SiteContentForm(
            request.POST,
            request.FILES,
            instance=content
        )
        if form.is_valid():
            form.save()
            return redirect("admin-main-page")
    else:
        form = SiteContentForm(instance=content)

    return render(request, "admin/main_page.html", {
        "form": form,
        "content": content
    })
    
    
    
    
from django.shortcuts import render, get_object_or_404, redirect
from .models import Role, CommunityMember
from .forms import CommunityMemberForm

# Main Community Page (show current year by default)
def community(request):
    latest_member = CommunityMember.objects.order_by('-year').first()
    current_year = latest_member.year if latest_member else None

    selected_year = request.GET.get('year')
    if selected_year and selected_year.isdigit():
        year = int(selected_year)
    else:
        year = current_year

    roles_with_members = Role.objects.prefetch_related('members').all()

    # Assign members of the selected year
    for role in roles_with_members:
        role.members_for_year = role.members.filter(year=year)

    available_years = CommunityMember.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'public/community.html', {
        'roles_with_members': roles_with_members,
        'year': year,
        'available_years': available_years,
    })

# Optional: Member Detail Page
def member_detail(request, member_id):
    member = get_object_or_404(CommunityMember, id=member_id)
    return render(request, 'member_detail.html', {'member': member})


def add_member(request):
    if not request.user.is_staff:
        return redirect('community')
    if request.method == "POST":
        form = CommunityMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_community')
    else:
        form = CommunityMemberForm()
    return render(request, 'public/add_member.html', {'form': form})


def edit_member(request, member_id):
    if not request.user.is_staff:
        return redirect('community')
    member = get_object_or_404(CommunityMember, id=member_id)
    if request.method == "POST":
        form = CommunityMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('admin_community')
    else:
        form = CommunityMemberForm(instance=member)
    return render(request, 'public/edit_member.html', {'form': form, 'member': member})


def delete_community_member(request, member_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('community')
    member = get_object_or_404(CommunityMember, id=member_id)
    if request.method == "POST":
        member_name = member.name
        member.delete()
        messages.success(request, f"'{member_name}' has been deleted successfully.")
        return redirect('admin_community')
    return render(request, 'public/confirm_delete.html', {'member': member})



from django.shortcuts import render
from .models import Role
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def admin_community(request):
    """
    Admin dashboard to manage members by role
    """
    roles_with_members = Role.objects.prefetch_related('members').all()
    return render(request, 'deshboard/admin_community.html', {'roles_with_members': roles_with_members})


from django.shortcuts import render
from .models import Role

def show_community_members(request):
    roles_with_members = Role.objects.prefetch_related('members').all()
    return render(request, 'public/community.html', {'roles_with_members': roles_with_members})




from django.shortcuts import render, get_object_or_404
from .models import Member
from .utils import fetch_codeforces_rating, fetch_codechef_rating, fetch_atcoder_rating

# Codeforces members page
def codeforces_members(request):
    members = Member.objects.all()
    for m in members:
        m.cf_rating = fetch_codeforces_rating(m.codeforces_handle)
    members_sorted = sorted(members, key=lambda x: x.cf_rating, reverse=True)
    return render(request, 'leaderboard/codeforces.html', {'members': members_sorted})

# Codechef members page
def codechef_members(request):
    members = Member.objects.all()
    for m in members:
        m.cc_rating = fetch_codechef_rating(m.codechef_handle)
    members_sorted = sorted(members, key=lambda x: x.cc_rating, reverse=True)
    return render(request, 'oj/codechef.html', {'members': members_sorted})

# Atcoder members page
def atcoder_members(request):
    members = Member.objects.all()
    for m in members:
        m.at_rating = fetch_atcoder_rating(m.atcoder_handle)
    members_sorted = sorted(members, key=lambda x: x.at_rating, reverse=True)
    return render(request, 'oj/atcoder.html', {'members': members_sorted})

# Member detail page (any OJ)
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.cf_rating = fetch_codeforces_rating(member.codeforces_handle)
    member.cc_rating = fetch_codechef_rating(member.codechef_handle)
    member.at_rating = fetch_atcoder_rating(member.atcoder_handle)
    return render(request, 'oj/member_detail.html', {'member': member})

def leaderboard(request):
    return render(request,'Core_templates/leaderboard.html')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Member
from .forms import MemberHandleForm


# Show all members + handles (list page)


@login_required
def handles_view(request):
    member = get_object_or_404(Member, user=request.user)
    return render(request, 'profile/online_judge_handle.html', {
        'member': member
    })


# Edit handles of a single member
@login_required
def edit_my_handles(request):
    member = get_object_or_404(Member, user=request.user)

    if request.method == 'POST':
        form = MemberHandleForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('handles')
    else:
        form = MemberHandleForm(instance=member)

    return render(request, 'profile/edit_handles.html', {'form': form})



def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    return render(request,'notice/notice_view.html', {'notice': notice})




from .forms import NoticeForm

# Admin notice list page
@login_required
def admin_notice_list(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'admin/admin_notice_list.html', {'notices': notices})

# Add notice
@login_required
def admin_notice_add(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            if notice.is_pinned:
                # Auto unpin previous
                Notice.objects.filter(is_pinned=True).update(is_pinned=False)
            notice.save()
            return redirect('admin_notice_list')
    else:
        form = NoticeForm()
    return render(request, 'admin/admin_notice_form.html', {'form': form, 'action': 'Add'})

# Edit notice
@login_required
def admin_notice_edit(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            if notice.is_pinned:
                Notice.objects.filter(is_pinned=True).exclude(id=notice.id).update(is_pinned=False)
            notice.save()
            return redirect('admin_notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'admin/admin_notice_form.html', {'form': form, 'action': 'Edit'})

# Delete notice
@login_required
def admin_notice_delete(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.method == 'POST':
        notice.delete()
        return redirect('admin_notice_list')
    return render(request, 'admin/admin_notice_delete.html', {'notice': notice})




from django.shortcuts import render
from .models import Member, UserSkill, Session
from .forms import MemberFilterForm

def admin_dashboard(request):
    # Filter form
    form = MemberFilterForm(request.GET or None)

    members = Member.objects.select_related('user', 'session').all()

    if form.is_valid():
        session = form.cleaned_data.get('session')
        if session:
            members = members.filter(session=session)

    # Stats (always defined, outside the if-block)
    total_users = Member.objects.count()
    active_members = Member.objects.filter(user__is_active=True).count()
    alumni_count = Member.objects.filter(status='alumni').count()
    total_skills = UserSkill.objects.count()

    context = {
        'form': form,
        'members': members,
        'total_users': total_users,
        'active_members': active_members,
        'alumni_count': alumni_count,
        'total_skills': total_skills,
    }
    return render(request, 'deshboard/deshboard.html', context)


from django.shortcuts import get_object_or_404

def delete_user_member(request, pk):
    """Delete Member model (User-based member) from admin dashboard"""
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('admin_dashboard')


from django.shortcuts import render, get_object_or_404
from .models import Member

def view_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'deshboard/admin_user_profile_edit.html', {'member': member})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import CustomUser, Member, JobProfile, UserSkill, UserAddress
from .forms import UserForm, MemberForm, JobProfileForm, UserSkillForm, UserAddressForm


@staff_member_required
def admin_user_profile_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    member, _ = Member.objects.get_or_create(user=user)

    # Forms
    user_form = UserForm(request.POST or None, instance=user)
    member_form = MemberForm(request.POST or None, request.FILES or None, instance=member)

    # JobProfiles
    job_profiles = JobProfile.objects.filter(user=user)
    if not job_profiles.exists():
        JobProfile.objects.create(user=user, job_title="", company_name="")
    job_forms = [JobProfileForm(request.POST or None, instance=j, prefix=f'job-{j.id}') for j in JobProfile.objects.filter(user=user)]

    # Skills
    skills_qs = UserSkill.objects.filter(user=user)
    if not skills_qs.exists():
        UserSkill.objects.create(user=user, skill_name="")
    skill_forms = [UserSkillForm(request.POST or None, instance=s, prefix=f'skill-{s.id}') for s in UserSkill.objects.filter(user=user)]

    # Addresses
    addresses_qs = UserAddress.objects.filter(user=user)
    if not addresses_qs.exists():
        UserAddress.objects.create(user=user, address_type="P", street="", city="", state="", country="")
    address_forms = [UserAddressForm(request.POST or None, instance=a, prefix=f'addr-{a.id}') for a in UserAddress.objects.filter(user=user)]

    if request.method == 'POST':
        valid = user_form.is_valid() and member_form.is_valid()
        valid = valid and all(f.is_valid() for f in job_forms + skill_forms + address_forms)

        if valid:
            user_form.save()
            member_form.save()
            for f in job_forms + skill_forms + address_forms:
                obj = f.save(commit=False)
                obj.user = user
                obj.save()
            return redirect('admin_user_detail', user_id=user.id)

    return render(request, 'deshboard/admin_user_profile_edit.html', {
        'user': user,
        'member': member,
        'user_form': user_form,
        'member_form': member_form,
        'job_forms': job_forms,
        'skill_forms': skill_forms,
        'address_forms': address_forms,
    })

# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Member, JobProfile, UserSkill, UserAddress

User = get_user_model()



@staff_member_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    member = Member.objects.filter(user=user).first()
    job_profiles = JobProfile.objects.filter(user=user)
    skills = UserSkill.objects.filter(user=user)
    addresses = UserAddress.objects.filter(user=user)
    return render(request, 'deshboard/admin_user_detail.html', {
        'user': user,
        'member': member,
        'job_profiles': job_profiles,
        'skills': skills,
        'addresses': addresses,
    })
    
    
    
def blog_list(request):
    return render(request,'Core_templates/blog.html')


    

    
    
    
    







    
    
    
