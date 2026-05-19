from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/',views.about),
    path('index/',views.index),
    path('alumina',views.alumina),
    path('login/',views.login_view,name = "login"),
    path('register/',views.register_view,name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_page',views.admin_dashboard,name="admin_page"),
    path('user_list/',views.user_list,name="user_list"),
    path('profile_index/',views.profile_index,name="profile_index"),
    path('personal_information/',views.personal_information,name="personal_information"),
  
    path('jobs/', views.job_list, name='job_list'),
    path('job/add/', views.job_add, name='job_add'),
    path('job/edit/<int:pk>/', views.job_edit, name='job_edit'),
    path('skill_create/',views.skill_add,name='skill_create'),
    path('show_skill/',views.skill_list,name='show_skill'),
    path('skill_edit/<int:pk>/', views.skill_edit, name='skill_edit'),
    path('address/',views.address_list,name='address_list'),
    path('addredd/add/',views.address_add,name='address_add'),
    path('address/edit/<int:pk>/',views.address_edit,name='address_edit'),
    path('proud_professionals/',views.proud_professionals, name='proud_professionals'),
    path('community_members/',views.community_members,name='community_members'),
    path('faculty_members/',views.faculty_members,name='faculty_members'),
    path('deshboard/',views.deshboard,name='deshboard'),
    path("main-page/",views.admin_main_page, name="admin-main-page"),
    path('navbar/',views.navbar),
    path('learning/',views.learning,name="learning"),
    path('blogs/',views.blogs,name="blogs"),
    
    path('community', views.community, name='community'),

    # Member detail page
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),

    # Staff-only member management pages
    path('member_add/', views.add_member, name='add_member'),
    path('member/<int:member_id>/edit/', views.edit_member, name='edit_member'),
    path('member/<int:member_id>/delete/', views.delete_community_member, name='delete_member'),
    path('admin_community/', views.admin_community, name='admin_community'),
    path('show_community/',views.show_community_members,name="show_community"),
    path('codeforces/', views.codeforces_members, name='codeforces_members'),
    path('codechef/', views.codechef_members, name='codechef_members'),
    path('atcoder/', views.atcoder_members, name='atcoder_members'),
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('leaderboard/',views.leaderboard,name="leaderboard"),
    path('handles/', views.handles_view, name='handles'),
    path('handles_edit/', views.edit_my_handles, name='edit_handles'),
    path('notice_view/<int:id>/', views.notice_detail, name='notice_detail'),

    path('admin_notices/', views.admin_notice_list, name='admin_notice_list'),
    path('admin_notices_add/', views.admin_notice_add, name='admin_notice_add'),
    path('admin_notices_edit/<int:id>/', views.admin_notice_edit, name='admin_notice_edit'),
    path('admin_notices_delete/<int:id>/', views.admin_notice_delete, name='admin_notice_delete'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_member/<int:member_id>/', views.view_member, name='view_member'),
    path('admin_delete_member/<int:member_id>/', views.delete_user_member, name='admin_delete_member'),
    path('edit_personal_information/', views.edit_personal_information, name='edit_personal_information'),

    path('admin_user_details/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin_user_profile_edit/<int:user_id>/', views.admin_user_profile_edit, name='admin_user_profile_edit'),
    path('blog_list/',views.blog_list,name="blog list"),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
