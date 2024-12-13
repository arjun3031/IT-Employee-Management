from django.urls import path
from .import views


urlpatterns = [
        path('', views.homepage, name='homepage'),  
        path('loginpage',views.loginpage,name='loginpage'),
        path('logout',views.logout,name='logout'),
        path('userlog',views.userlog,name='userlog'),
        path('signuppage',views.signuppage,name='signuppage'),
        path('usercreate',views.usercreate,name='usercreate'),
        path('about',views.about,name='about'),
        path('service',views.service,name='service'),
        path('contact',views.contact,name='contact'),



        path('adminhome',views.adminhome,name='adminhome'),
        path('manageuser',views.manageuser,name='manageuser'),
        path('userrequest',views.userrequest,name='userrequest'),
        path('acceptworker/<int:accept>/', views.acceptworker, name='acceptworker'),
        path('rejectworker/<int:reject>/', views.rejectworker, name='rejectworker'),
        path('viewworker', views.viewworker, name='viewworker'),
        path('deleteworker/<int:delete>/', views.deleteworker, name='deleteworker'),

        path('manageproject',views.manageproject,name='manageproject'),
        path('addproject', views.addproject, name='addproject'),
        path('viewproject', views.viewproject, name='viewproject'),
        path('editproject/<int:project_id>/', views.editproject, name='editproject'),
        path('deleteproject/<int:project_id>/', views.deleteproject, name='deleteproject'),
        path('viewclients', views.viewclients, name='viewclients'),
        path('assignproject', views.assignproject, name='assignproject'),

        path('pythondeppartment',views.pythondeppartment,name='pythondeppartment'),
        path('assign_role',views.assign_role,name='assign_role'),
        path('python_users',views.python_users,name='python_users'),
        path('viewdevelopers', views.viewdevelopers, name='viewdevelopers'),
        path('assign_developers_to_team/', views.assign_developers_to_team, name='assign_developers_to_team'),
        path('get_project/<int:team_leader_id>/', views.get_project, name='get_project'),
        path('view_work_reports_by_admin', views.view_work_reports_by_admin, name='view_work_reports_by_admin'),
        path('view_all_team_leaders_daily_reports', views.view_all_team_leaders_daily_reports, name='view_all_team_leaders_daily_reports'),
        path('python_employees', views.python_employees, name='python_employees'),
        path('show_teamleaders', views.show_teamleaders, name='show_teamleaders'),
        path('show_developers', views.show_developers, name='show_developers'),




        path('teamleaderhome',views.teamleaderhome,name='teamleaderhome'),
        path('teamleaderprofile/<int:sp>/', views.teamleaderprofile, name='teamleaderprofile'),
        path('teamleaderprofileedit/<int:se>',views.teamleaderprofileedit,name='teamleaderprofileedit'),
        path('update_teamleader/<int:se>/', views.update_teamleader, name='update_teamleader'),
        path('reset_password_team_leader', views.reset_password_team_leader, name='reset_password_team_leader'),
        # path('view_assigned_projects/', views.view_assigned_projects, name='view_assigned_projects'),
        # path('project/<int:project_id>/complete/', views.complete_project, name='complete_project'),
        path('view_assigned_projects/', views.view_assigned_projects, name='view_assigned_projects'),
        path('project/<int:project_id>/complete/', views.complete_project, name='complete_project'),

        path('view_assigned_developers', views.view_assigned_developers, name='view_assigned_developers'),
        path('assign_work', views.assign_work, name='assign_work'),
        path('view_submitted_works', views.view_submitted_works, name='view_submitted_works'),
        path('verify_work/<int:work_id>/', views.verify_work, name='verify_work'),
        path('view_verified_works', views.view_verified_works, name='view_verified_works'), 
        path('developer-reports/', views.view_developer_reports, name='view_developer_reports'),
        path('update_daily_report_teamleader', views.update_daily_report_teamleader, name='update_daily_report_teamleader'),
        path('view_teamleaders_daily_reports', views.view_teamleaders_daily_reports, name='view_teamleaders_daily_reports'),






        path('developerhome/', views.developerhome, name='developerhome'),
        path('developer/<int:dp>/', views.developerprofile, name='developerprofile'),
        path('developereditprofile/<int:dp>/', views.developereditprofile, name='developereditprofile'),
        path('update_developer/<int:dp>/', views.update_developer, name='update_developer'),
        path('reset_password_developer/', views.reset_password_developer, name='reset_password_developer'),
        path('assigned_project_for_developer', views.assigned_project_for_developer, name='assigned_project_for_developer'),
        path('team-leader-details/<int:developer_id>/', views.view_team_leader_details, name='team_leader_details'),
        path('view_assigned_work', views.view_assigned_work, name='view_assigned_work'),
        path('view_submitted_works_by_developer', views.view_submitted_works_by_developer, name='view_submitted_works_by_developer'), 
        path('update_daily_report', views.update_daily_report, name='update_daily_report'),
        path('get_team_leader/<int:project_id>/', views.get_team_leader, name='get_team_leader'),
        path('view_daily_reports', views.view_daily_reports, name='view_daily_reports'),


]
