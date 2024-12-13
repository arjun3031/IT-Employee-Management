from django.shortcuts import render,redirect,get_object_or_404
from app.models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import re,os
from django.http import JsonResponse
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from datetime import date
from django.utils.dateparse import parse_date  




# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def loginpage(request):
    return render(request,'loginpage.html')

def logout(request):
    auth.logout(request)
    return redirect('homepage')

# def userlog(request):
#     if request.method == 'POST':
#         usname = request.POST['username']
#         passwrd = request.POST['password']
#         user = auth.authenticate(username=usname, password=passwrd)

#         if user is not None:
#             if user.is_staff:
#                 auth.login(request, user)
#                 return redirect('adminhome')  

#             worker_exists = Workers.objects.filter(user=user).exists()
#             if worker_exists:
#                 worker = Workers.objects.get(user=user) 

#                 if worker.status != 'Accepted':
#                     messages.info(request, 'Your account is not accepted yet.')
#                     return redirect('loginpage')

#                 python_worker = worker.user.python_set.first() 
#                 if python_worker and python_worker.role == 'Team Leader':
#                     auth.login(request, user) 
#                     messages.success(request, "New project is assigned on you!")
#                     return redirect('teamleaderhome') 
#                 elif python_worker and python_worker.role == 'Developer':
#                     auth.login(request, user) 
#                     return redirect('developerhome')
#             else:
#                 messages.info(request, 'You do not have permission to login.')
#                 return redirect('loginpage')
#         else:
#             messages.info(request, 'Invalid username or password')
#             return redirect('loginpage')
#     else:
#         return redirect('loginpage')

def userlog(request):
    if request.method == 'POST':
        usname = request.POST['username']
        passwrd = request.POST['password']
        user = auth.authenticate(username=usname, password=passwrd)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')

            worker_exists = Workers.objects.filter(user=user).exists()
            if worker_exists:
                worker = Workers.objects.get(user=user)

                if worker.status != 'Accepted':
                    messages.info(request, 'Your account is not accepted yet.')
                    return redirect('loginpage')

                python_worker = worker.user.python_set.first()

                if python_worker:
                    if python_worker.role == 'Team Leader':
                        login(request, user)
                        # messages.success(request, "New project is assigned to you!")
                        return redirect('teamleaderhome')
                    elif python_worker.role == 'Developer':
                        login(request, user)
                        return redirect('developerhome')
                    else:
                        messages.error(request, "Unable to login. No role assigned.")
                        return redirect('loginpage')
                else:
                    messages.error(request, "Unable to login. No role assigned.")
                    return redirect('loginpage')
            else:
                messages.info(request, 'You do not have permission to login.')
                return redirect('loginpage')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('loginpage')
    else:
        return redirect('loginpage')

def signuppage(request):
    return render(request,'signuppage.html')

def usercreate(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['uname']
        addresses = request.POST['address']
        mobile = request.POST['mobile']
        mail = request.POST['mail']
        department = request.POST['department']
        course_completed = request.POST['coursecompleted']  
        img = request.FILES.get('img')
        certificate = request.FILES.get('certificate')  
        
        password = get_random_string(length=6)
        
        if username == mail:
            messages.info(request, 'Username and email cannot be the same')
            return redirect('signuppage')
    
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('signuppage')
        
        if Workers.objects.filter(mobile=mobile).exists():
            messages.info(request, 'Mobile number already exists')
            return redirect('signuppage')
        
        if User.objects.filter(email=mail).exists():
            messages.info(request, 'Email already exists')
            return redirect('signuppage')
        
        if '.com' not in mail:
            messages.error(request, 'Email format is incorrect')
            return redirect('signuppage')

        user = User.objects.create_user(first_name=firstname,last_name=lastname,email=mail,username=username)
        user.set_password(password)
        user.save()

        Workers.objects.create(user=user,mobile=mobile,address=addresses,department=department,course_completed=course_completed,certificate=certificate,image=img)
        
        send_mail(
            'New Account Credentials',
            f'New user registration details:\n\nUsername: {username}\nPassword: {password}',
            'arjunkmvat@gmail.com',  
            ['arjunkmvat@gmail.com'],
            fail_silently=False,
            )
        messages.success(request, 'Account created successfully! Check email for password')
        return redirect('signuppage')
    else:
        return render(request, 'signuppage.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def contact(request):
    return render(request,'contact.html')







@login_required(login_url='homepage')
def adminhome(request): 
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()    
    return render(request, 'adminhome.html', {'pending_count': count,'projuct_count':pcount})

@login_required(login_url='homepage')
def manageuser(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()   
    return render(request, 'manageuser.html', {'pending_count': count,'projuct_count':pcount})

def userrequest(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()    
    pending=Workers.objects.filter(status='Pending')
    return render(request, 'userrequest.html', {'pending_count': count,'projuct_count':pcount,'pworkers': pending})

def acceptworker(request, accept):
    worker = Workers.objects.get(id=accept)
    worker.status = 'Accepted'
    worker.save()    
    messages.success(request, f"Worker '{worker.user.first_name} {worker.user.last_name}' has been accepted.")
    return redirect('userrequest')

# def rejectworker(request, reject):
#     worker = Workers.objects.get(id=reject)
#     worker.delete()
#     User.objects.get(id=worker.user.id).delete()
#     return redirect('userrequest')


def rejectworker(request, reject):
    worker = get_object_or_404(Workers, id=reject)
    user = worker.user  
    worker.delete()    
    User.objects.get(id=user.id).delete()    
    messages.error(request, f"Worker '{user.first_name} {user.last_name}' has been rejected & deleted.")
    return redirect('userrequest')

@login_required(login_url='homepage')
def viewworker(request):
    departments = ['Digital marketing', 'Python']
    selected_department = request.GET.get('department')
    count = Workers.objects.filter(status='Pending').count()   
    pcount = Project.objects.filter(project_status='Pending').count()
    if selected_department:
        accepted_workers = Workers.objects.filter(status='Accepted', department=selected_department).select_related('user').distinct()
    else:
        accepted_workers = Workers.objects.filter(status='Accepted').select_related('user').distinct()
    return render(request, 'viewworkers.html',{'accepted_workers': accepted_workers,'departments': departments,'selected_department': selected_department,'worker_pending_count': count,'pending_count': count,'projuct_count':pcount})


def deleteworker(request, delete):
    worker = get_object_or_404(Workers, id=delete)
    ongoing_projects = Project.objects.filter(worker=worker, project_status__in=['Pending', 'Ongoing']).exists()

    if ongoing_projects:
        messages.error(request, "The worker is currently assigned to an active project.")
    else:
        User.objects.get(id=worker.user.id).delete() 
        worker.delete()  
        messages.success(request, f"Worker '{worker.user.username}' has been successfully deleted.")
    return redirect('viewworker')

@login_required(login_url='homepage')
def manageproject(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()   
    return render(request, 'manageproject.html', {'pending_count': count,'projuct_count':pcount})

def addproject(request):
    workers = Workers.objects.all()
    count = Workers.objects.filter(status='Pending').count()   
    pcount = Project.objects.filter(project_status='Pending').count()  

    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        client_address = request.POST.get('client_address')
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        attachment = request.FILES.get('attachment')

        if Workers.objects.filter(mobile=client_phone).exists():
            messages.error(request, "This mobile number is already registered")
            return render(request, 'addproject.html', {
                'workers': workers,
                'client_name': client_name,
                'client_email': client_email,
                'client_phone': client_phone,
                'client_address': client_address,
                'description': description,
                'requirements': requirements,
                'start_date': start_date,
                'end_date': end_date,
                'pending_count': count,
                'project_count': pcount
            })

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date_obj >= end_date_obj:
            messages.error(request, "Start date must be less than the end date.")
            return render(request, 'addproject.html', {
                'workers': workers,
                'client_name': client_name,
                'client_email': client_email,
                'client_phone': client_phone,
                'client_address': client_address,
                'description': description,
                'requirements': requirements,
                'start_date': start_date,
                'end_date': end_date
            })

        if '.com' not in client_email:
            messages.error(request, 'Email must contain .com')
            return redirect('addproject')

        if attachment:
            fs = FileSystemStorage()
            attachment_name = fs.save(attachment.name, attachment)
            attachment_url = fs.url(attachment_name)
        else:
            attachment_url = None

        Project.objects.create(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            client_address=client_address,
            project_name=project_name,
            description=description,
            requirements=requirements,
            start_date=start_date_obj,
            end_date=end_date_obj,
            attachment=attachment,
            project_status='Pending' 
        )

        messages.success(request, "Project added successfully!")
        return redirect('addproject')

    return render(request, 'addproject.html', {'workers': workers, 'pending_count': count, 'project_count': pcount})

@login_required(login_url='homepage')
def viewproject(request):
    projects = Project.objects.all()
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    project_name = request.GET.get('project_name', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    project_status = request.GET.get('project_status', '')  

    if project_name:
        projects = projects.filter(project_name__icontains=project_name)  
    
    if start_date:
        projects = projects.filter(start_date__gte=start_date)
    
    if end_date:
        projects = projects.filter(end_date__lte=end_date)

    if project_status:
        projects = projects.filter(project_status=project_status)  

    project_names = Project.objects.values_list('project_name', flat=True).distinct()
    project_statuses = ['Pending', 'Ongoing', 'Completed']  

    return render(request, 'viewproject.html', {
        'projects': projects,
        'project_count': pcount,
        'project_name': project_name,
        'start_date': start_date,
        'end_date': end_date,
        'project_status': project_status,  
        'project_names': project_names,
        'project_statuses': project_statuses,'pending_count': count,'projuct_count':pcount
    })

def editproject(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.client_name = request.POST.get('client_name')
        project.client_email = request.POST.get('client_email')
        project.client_phone = request.POST.get('client_phone')
        project.client_address = request.POST.get('client_address')
        project.project_name = request.POST.get('project_name')
        project.description = request.POST.get('description')
        project.requirements = request.POST.get('requirements')
        project.start_date = request.POST.get('start_date')
        project.end_date = request.POST.get('end_date')
        attachment = request.FILES.get('attachment')

        if attachment:
            fs = FileSystemStorage()
            attachment_name = fs.save(attachment.name, attachment)
            project.attachment = fs.url(attachment_name)
        project.save()
        messages.success(request, "Project updated successfully!")
        return redirect('viewproject')
    return render(request, 'editproject.html', {'project': project})

@login_required(login_url='homepage')
def deleteproject(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect('viewproject')

def viewclients(request):
    selected_client = request.GET.get('client', '')
    selected_status = request.GET.get('project_status', '')
    
    projects = Project.objects.all()
    clients = Project.objects.values('client_name').distinct()
    pending_worker_count = Workers.objects.filter(status='Pending').count()
    pending_project_count = Project.objects.filter(project_status='Pending').count()
    
    if selected_client:
        projects = projects.filter(client_name=selected_client)
        
    if selected_status:
        projects = projects.filter(project_status=selected_status)

    if not projects.exists():
        messages.info(request, "No projects found for the selected filters.")
    
    return render(request, 'viewclient.html', {
        'projects': projects,
        'clients': clients,
        'selected_client': selected_client,
        'selected_status': selected_status,
        'pending_count': pending_worker_count,
        'project_count': pending_project_count
    })


# @login_required(login_url='homepage')
# def assignproject(request):
#     count = Workers.objects.filter(status='Pending').count()   
#     pcount = Project.objects.filter(project_status='Pending').count()
    
#     if request.method == "POST":
#         project_id = request.POST.get("project_id")
#         worker_id = request.POST.get("worker_id")
#         project = Project.objects.get(id=project_id)
#         worker = Workers.objects.get(id=worker_id)        
#         project.worker = worker
#         project.project_status = 'Ongoing'
#         project.save()
#         team, created = Team.objects.get_or_create(
#             project=project,
#             defaults={'team_leader': worker}
#         )
        
#         if not created:
#             team.team_leader = worker
#             team.save()
#         messages.success(request, f'Project "{project.project_name}" has been successfully assigned to {worker.user.username}!')
#         return redirect('assignproject')
#     pending_projects = Project.objects.filter(project_status='Pending')
#     available_team_leaders = Workers.objects.filter(
#         status='Accepted'
#     ).filter(
#         user__python__role='Team Leader'
#     ).exclude(
#         id__in=Project.objects.filter(worker__isnull=False).values('worker')
#     )
#     return render(request, 'assignproject.html', {
#         'pending_projects': pending_projects,
#         'available_team_leaders': available_team_leaders,
#         'pending_count': count,
#         'projuct_count': pcount
#     })


@login_required(login_url='homepage')
def assignproject(request):
    count = Workers.objects.filter(status='Pending').count()   
    pcount = Project.objects.filter(project_status='Pending').count()
    
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        worker_id = request.POST.get("worker_id")
        project = Project.objects.get(id=project_id)
        worker = Workers.objects.get(id=worker_id)        
        project.worker = worker
        project.project_status = 'Ongoing'
        project.save()
        team, created = Team.objects.get_or_create(
            project=project,
            defaults={'team_leader': worker}
        )
        
        if not created:
            team.team_leader = worker
            team.save()
        messages.success(request, f'Project "{project.project_name}" has been successfully assigned to {worker.user.username}!')
        return redirect('assignproject')

    pending_projects = Project.objects.filter(project_status='Pending')

    available_team_leaders = Workers.objects.filter(
        status='Accepted',
        user__python__role='Team Leader'
    ).exclude(
        id__in=Project.objects.filter(worker__isnull=False).values('worker')
    )

    completed_projects_leaders = Workers.objects.filter(
        id__in=Project.objects.filter(project_status='Completed').values('worker')
    )

    available_team_leaders = available_team_leaders | completed_projects_leaders

    return render(request, 'assignproject.html', {
        'pending_projects': pending_projects,
        'available_team_leaders': available_team_leaders.distinct(),
        'pending_count': count,
        'projuct_count': pcount
    })


@login_required(login_url='homepage')
def pythondeppartment(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()   
    return render(request, 'pythondepartment.html', {'pending_count': count,'projuct_count':pcount})

@login_required(login_url='homepage')
def assign_role(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()    
    python_workers = Workers.objects.filter(
        status='Accepted', 
        department='Python'
    ).exclude(
        user_id__in=Python.objects.values_list('user_id', flat=True)  
    ).select_related('user')
    
    roles = ['Developer', 'Team Leader'] 
    
    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        new_role = request.POST.get("role")
        if worker_id and new_role:
            python_worker, created = Python.objects.get_or_create(user_id=worker_id)        
            python_worker.role = new_role
            python_worker.save()

            messages.success(request, 'Role updated successfully!')
        else:
            messages.error(request, 'Please select a valid worker and role.')

        return redirect('assign_role')  

    return render(request, 'assign_role.html', {
        'python_workers': python_workers,
        'roles': roles,
        'pending_count': count,
        'project_count': pcount
    })

@login_required(login_url='homepage')
def python_users(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    python_workers = Workers.objects.filter(department='Python', status='Accepted').select_related('user')
    selected_worker = None
    assigned_projects = None
    role = None

    if request.method == "POST":
        selected_worker_id = request.POST.get('worker_id')
        if selected_worker_id:
            selected_worker = Workers.objects.filter(id=selected_worker_id).select_related('user').first()
            if selected_worker:
                role = Python.objects.filter(user=selected_worker.user).first()
                if role and role.role == 'Team Leader':
                    assigned_projects = Project.objects.filter(team__team_leader=selected_worker)
                else:
                    assigned_projects = Project.objects.filter(team__python__user=selected_worker.user).distinct()
        else:
            messages.error(request, "Please select a worker.")
    return render(request, 'pythonusers.html', {
        'python_workers': python_workers,
        'selected_worker': selected_worker,
        'assigned_projects': assigned_projects,
        'role': role,
        'pending_count': count,
        'project_count': pcount,})

# @login_required(login_url='homepage')
# def viewdevelopers(request):
#     count = Workers.objects.filter(status='Pending').count()
#     pcount = Project.objects.filter(project_status='Pending').count()
    
#     selected_role = request.GET.get('role', None)

#     python_developers = Workers.objects.filter(
#         status='Accepted', 
#         department='Python'
#     ).select_related('user').distinct()

#     if selected_role:
#         python_developers = python_developers.filter(
#             user__python__role=selected_role  
#         )

#     if request.method == "POST":
#         worker_id = request.POST.get("worker_id")
#         python_worker = Python.objects.get(user_id=worker_id)
#         assigned_project = Project.objects.filter(
#             worker__user__id=worker_id, 
#             project_status__in=['Pending', 'Ongoing']
#         ).exists()

#         if assigned_project:
#             messages.error(request, 'This employee is working on a project. Role changes are only allowed when the project is completed.')
#         else:
#             if python_worker.role == 'Developer':
#                 python_worker.role = 'Team Leader'
#             else:
#                 python_worker.role = 'Developer'

#             python_worker.save()
#             messages.success(request, 'Role updated successfully!')

#         return redirect('viewdevelopers')

#     python_developers_with_roles = []
#     for worker in python_developers:
#         role = Python.objects.filter(user=worker.user).first()
#         python_developers_with_roles.append({
#             'worker': worker,
#             'role': role.role if role else 'Not Assigned'  
#         })

#     return render(request, 'viewdevelopers.html', {
#         'python_developers_with_roles': python_developers_with_roles, 
#         'pending_count': count,
#         'project_count': pcount,
#         'selected_role': selected_role,
#     })

# def assign_developers_to_team(request):
#     count = Workers.objects.filter(status='Pending').count()
#     pcount = Project.objects.filter(project_status='Pending').count()
#     team_leaders = Python.objects.filter(role='Team Leader').annotate(developer_count=Count('team__python')).filter(developer_count__lt=4)
#     available_developers = Python.objects.filter(role='Developer', team__isnull=True)

#     if request.method == 'POST':
#         team_leader_id = request.POST.get('team_leader')
#         developer_id = request.POST.get('developers')
#         team_leader = get_object_or_404(Workers, user__id=team_leader_id)
#         project = Project.objects.filter(worker=team_leader).first() 

#         if project:
#             team, created = Team.objects.get_or_create(team_leader=team_leader, project=project)
#             developer = get_object_or_404(Python, id=developer_id)
#             developer.team = team
#             developer.save()

#             messages.success(request, f"{developer.user.first_name} {developer.user.last_name} has been assigned to the team successfully")
#         else:
#             messages.error(request, "No project found for the selected team leader.")

#     return render(request, 'assign_developers_to_team.html', {
#         'team_leaders': team_leaders,
#         'available_developers': available_developers,
#         'pending_count': count,
#         'project_count': pcount
#     })

# @login_required
# def assign_developers_to_team(request):
#     count = Workers.objects.filter(status='Pending').count()
#     pcount = Project.objects.filter(project_status='Pending').count()

#     team_leaders = Python.objects.filter(role='Team Leader').annotate(developer_count=Count('team__python')).filter(developer_count__lt=4)
    
#     unassigned_developers = Python.objects.filter(role='Developer', team__isnull=True)
    
#     developers_with_completed_projects = Python.objects.filter(
#         role='Developer',
#         team__project__project_status='Completed'
#     )

#     available_developers = (unassigned_developers | developers_with_completed_projects).distinct()

#     if request.method == 'POST':
#         team_leader_id = request.POST.get('team_leader')
#         developer_id = request.POST.get('developers')
#         team_leader = get_object_or_404(Workers, user__id=team_leader_id)
#         project = Project.objects.filter(worker=team_leader).first() 

#         if project:
#             team, created = Team.objects.get_or_create(team_leader=team_leader, project=project)
#             developer = get_object_or_404(Python, id=developer_id)
#             developer.team = team
#             developer.save()

#             messages.success(request, f"{developer.user.first_name} {developer.user.last_name} has been assigned to the team successfully")
#         else:
#             messages.error(request, "No project found for the selected team leader.")

#     return render(request, 'assign_developers_to_team.html', {
#         'team_leaders': team_leaders,
#         'available_developers': available_developers,
#         'pending_count': count,
#         'project_count': pcount
#     })

# def viewdevelopers(request):
#     count = Workers.objects.filter(status='Pending').count()
#     pcount = Project.objects.filter(project_status='Pending').count()
    
#     selected_role = request.GET.get('role', None)

#     python_developers = Workers.objects.filter(
#         status='Accepted', 
#         department='Python'
#     ).select_related('user').distinct()

#     if selected_role:
#         python_developers = python_developers.filter(
#             user__python__role=selected_role  
#         )

#     if request.method == "POST":
#         worker_id = request.POST.get("worker_id")
#         python_worker = Python.objects.get(user_id=worker_id)
        
#         active_project_exists = Project.objects.filter(
#             worker__user_id=worker_id, 
#             project_status__in=['Pending', 'Ongoing']
#         ).exists()

#         completed_project_exists = Project.objects.filter(
#             worker__user_id=worker_id,
#             project_status='Completed'
#         ).exists()

#         if active_project_exists:
#             messages.error(request, 'This employee is working on an active project. Role changes are only allowed when the project is completed.')
#         else:
#             if python_worker.role == 'Developer':
#                 python_worker.role = 'Team Leader'
#                 messages.success(request, 'Promoted to Team Leader successfully!')
#             else:
#                 python_worker.role = 'Developer'
#                 messages.success(request, 'Demoted to Developer successfully!')

#             python_worker.save()
#         return redirect('viewdevelopers')

#     python_developers_with_roles = []
#     for worker in python_developers:
#         role = Python.objects.filter(user=worker.user).first()
#         python_developers_with_roles.append({
#             'worker': worker,
#             'role': role.role if role else 'Not Assigned'  
#         })

#     return render(request, 'viewdevelopers.html', {
#         'python_developers_with_roles': python_developers_with_roles, 
#         'pending_count': count,
#         'project_count': pcount,
#         'selected_role': selected_role,
#     })

@login_required(login_url='homepage')
def viewdevelopers(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    
    selected_role = request.GET.get('role', None)
    
    python_developers = Workers.objects.filter(
        status='Accepted', 
        department='Python'
    ).select_related('user').distinct()

    if selected_role:
        python_developers = python_developers.filter(
            user__python__role=selected_role  
        )

    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        python_worker = Python.objects.get(user_id=worker_id)
        
        active_project_exists = Project.objects.filter(
            worker__user_id=worker_id, 
            project_status__in=['Pending', 'Ongoing']
        ).exists()
        completed_project_exists = Project.objects.filter(
            worker__user_id=worker_id,
            project_status='Completed'
        ).exists()
        
        team_assignment_exists = Team.objects.filter(
            python__user_id=worker_id,
            project__project_status__in=['Pending', 'Ongoing']
        ).exists()

        if active_project_exists or team_assignment_exists:
            messages.error(request, 'This employee is working on an active project. Role changes are only allowed when the project is completed.')
        else:
            if python_worker.role == 'Developer':
                python_worker.role = 'Team Leader'
                messages.success(request, 'Promoted to Team Leader successfully!')
            else:
                if completed_project_exists or not active_project_exists:
                    python_worker.role = 'Developer'
                    messages.success(request, 'Demoted to Developer successfully!')
                else:
                    messages.error(request, 'This team leader is still assigned to a project. Demotion is only allowed when the project is completed.')
            python_worker.save()

        return redirect('viewdevelopers')

    python_developers_with_roles = []
    for worker in python_developers:
        role = Python.objects.filter(user=worker.user).first()
        python_developers_with_roles.append({
            'worker': worker,
            'role': role.role if role else 'Not Assigned'  
        })

    return render(request, 'viewdevelopers.html', {
        'python_developers_with_roles': python_developers_with_roles, 
        'pending_count': count,
        'project_count': pcount,
        'selected_role': selected_role,
    })



@login_required(login_url='homepage')
def assign_developers_to_team(request):
    pending_worker_count = Workers.objects.filter(status='Pending').count()
    pending_project_count = Project.objects.filter(project_status='Pending').count()

    team_leaders = Python.objects.filter(
        role='Team Leader'
    ).annotate(
        developer_count=Count('team__python')
    ).filter(developer_count__lt=4)

    unassigned_developers = Python.objects.filter(
        role='Developer', 
        team__isnull=True
    )
    
    developers_with_completed_projects = Python.objects.filter(
        role='Developer',
        team__project__project_status='Completed'
    ).exclude(
        team__project__project_status__in=['Pending', 'Ongoing']
    )

    available_developers = (unassigned_developers | developers_with_completed_projects).distinct()

    if request.method == 'POST':
        team_leader_id = request.POST.get('team_leader')
        developer_id = request.POST.get('developers')

        team_leader = get_object_or_404(Workers, user__id=team_leader_id)
        project = Project.objects.filter(worker=team_leader, project_status='Ongoing').first()

        if project:
            team, created = Team.objects.get_or_create(team_leader=team_leader, project=project)
            developer = get_object_or_404(Python, id=developer_id)

            if developer.team and developer.team.project == project:
                messages.warning(request, f"{developer.user.first_name} {developer.user.last_name} is already assigned to this project.")
            else:
                developer.team = team
                developer.save()
                messages.success(request, f"{developer.user.first_name} {developer.user.last_name} has been successfully assigned to the team.")
        else:
            messages.error(request, "No active project found for the selected team leader.")

    return render(request, 'assign_developers_to_team.html', {
        'team_leaders': team_leaders,
        'available_developers': available_developers,
        'pending_worker_count': pending_worker_count,
        'pending_project_count': pending_project_count
    })


def get_project(request, team_leader_id):
    try:
        project = Project.objects.filter(worker__user__id=team_leader_id).first()
        if project:
            data = {
                'project_name': project.project_name
            }
        else:
            data = {
                'project_name': 'No project assigned'
            }
    except :
        data = {'project_name': 'No project found'}
    return JsonResponse(data)

def view_work_reports_by_admin(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    daily_reports = DailyReport.objects.select_related('developer', 'project', 'team_leader').order_by('report_date')
    team_leaders = DailyReport.objects.values(
        'team_leader__id', 'team_leader__user__first_name', 'team_leader__user__last_name'
    ).distinct()
    
    developers = DailyReport.objects.values(
        'developer__id', 'developer__user__first_name', 'developer__user__last_name'
    ).distinct()
    
    projects = DailyReport.objects.values(
        'project__id', 'project__project_name'
    ).distinct()

    team_leader_id = request.GET.get('team_leader', '')
    project_id = request.GET.get('project', '')
    developer_id = request.GET.get('developer', '')

    if team_leader_id:
        daily_reports = daily_reports.filter(team_leader__id=team_leader_id)
    if project_id:
        daily_reports = daily_reports.filter(project__id=project_id)
    if developer_id:
        daily_reports = daily_reports.filter(developer__id=developer_id)

    return render(request, 'view_work_reports_by_admin.html', {
        'daily_reports': daily_reports,
        'team_leaders': team_leaders,
        'developers': developers,
        'projects': projects,
        'team_leader_id': team_leader_id,
        'project_id': project_id,
        'developer_id': developer_id,'pending_count': count,
        'project_count': pcount})

def view_all_team_leaders_daily_reports(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    daily_reports = DailyReportTeamLeader.objects.select_related('team_leader', 'project').order_by('report_date')
    project_id = request.GET.get('project')
    team_leader_id = request.GET.get('team_leader')

    if project_id:
        daily_reports = daily_reports.filter(project__id=project_id)
    if team_leader_id:
        daily_reports = daily_reports.filter(team_leader__id=team_leader_id)

    projects = Project.objects.all()
    team_leaders = DailyReportTeamLeader.objects.values(
        'team_leader__id', 'team_leader__user__first_name', 'team_leader__user__last_name'
    ).distinct()

    return render(request, 'view_all_team_leaders_daily_reports.html', {
        'daily_reports': daily_reports,
        'projects': projects,
        'team_leaders': team_leaders,
        'project_id': project_id,
        'team_leader_id': team_leader_id,'pending_count': count,
        'project_count': pcount})

@login_required(login_url='homepage')
def python_employees(request):
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    python_workers = Workers.objects.filter(department='Python', status='Accepted')
    filter_type = request.GET.get('filter_type', 'teamleader')  
    workers_data = []
    no_data_message = None

    if filter_type == 'teamleader':
        team_leaders = python_workers.filter(user__python__role='Team Leader')
        for leader in team_leaders:
            projects = Project.objects.filter(team__team_leader=leader)
            project_names = []
            for project in projects:
                if project.project_status == 'Completed':
                    project_names.append(f"{project.project_name} (Completed)")
                else:
                    project_names.append(project.project_name)
            project_names_display = ', '.join(project_names) if project_names else 'No Project Assigned'
            workers_data.append({
                'full_name': f"{leader.user.first_name} {leader.user.last_name}",
                'email': leader.user.email,
                'mobile': leader.mobile,
                'address': leader.address,
                'project_names': project_names_display,
                'role': 'Team Leader',
            })

    elif filter_type == 'developer':
        developers = Python.objects.filter(role='Developer')
        for developer in developers:
            worker = developer.user.workers_set.first()
            if worker:
                projects = Project.objects.filter(team__python=developer).distinct()
                project_names = []
                for project in projects:
                    if project.project_status == 'Completed':
                        project_names.append(f"{project.project_name} (Completed)")
                    else:
                        project_names.append(project.project_name)
                project_names_display = ', '.join(project_names) if project_names else 'No Project Assigned'
                workers_data.append({
                    'full_name': f"{worker.user.first_name} {worker.user.last_name}",
                    'email': worker.user.email,
                    'mobile': worker.mobile,
                    'address': worker.address,
                    'project_names': project_names_display,
                    'role': developer.role,
                })

    if not workers_data:
        no_data_message = "No data available for the selected role."

    return render(request, 'python_employees.html', {
        'workers_data': workers_data,
        'filter_type': filter_type,
        'no_data_message': no_data_message,
        'pending_count': count,
        'project_count': pcount
    })


def show_teamleaders(request):
    python_workers = Workers.objects.filter(department='Python', status='Accepted')
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    selected_project = request.GET.get('project', '') 
    workers_data = []
    no_data_message = None
    projects = Project.objects.all()  
    team_leaders = python_workers.filter(user__python__role='Team Leader')

    if selected_project:
        team_leaders = team_leaders.filter(team__project__project_name=selected_project)

    for leader in team_leaders:
        assigned_projects = Project.objects.filter(team__team_leader=leader)
        project_names = []
        
        for project in assigned_projects:
            project_name_display = project.project_name
            if project.project_status == 'Completed':
                project_name_display += ' (Completed)'
            project_names.append(project_name_display)

        project_names_str = ', '.join(project_names) if project_names else 'No Project Assigned'
        workers_data.append({
            'full_name': f"{leader.user.first_name} {leader.user.last_name}",
            'email': leader.user.email,
            'mobile': leader.mobile,
            'address': leader.address,
            'project_names': project_names_str,
            'role': 'Team Leader'
        })

    if not workers_data:
        no_data_message = "No team leaders available for the selected project."

    return render(request, 'show_teamleaders.html', {
        'workers_data': workers_data,
        'no_data_message': no_data_message,
        'projects': projects, 
        'selected_project': selected_project,
        'pending_count': count,
        'project_count': pcount
    })

def show_developers(request):
    team_leaders = Python.objects.filter(role='Team Leader')  
    projects = Project.objects.all()  
    count = Workers.objects.filter(status='Pending').count()
    pcount = Project.objects.filter(project_status='Pending').count()
    selected_team_leader = request.GET.get('team_leader') 
    selected_project = request.GET.get('project') 
    developers = Python.objects.filter(role='Developer')

    if selected_team_leader:
        developers = developers.filter(team__team_leader__user__id=selected_team_leader)

    if selected_project:
        developers = developers.filter(team__project__id=selected_project)

    developers_data = []
    for developer in developers:
        project_name = "No project assigned"
        if developer.team and developer.team.project:
            project = developer.team.project
            project_name = project.project_name
            if project.project_status == 'Completed':
                project_name += ' (Completed)'

        developers_data.append({
            'full_name': f"{developer.user.first_name} {developer.user.last_name}",
            'email': developer.user.email,
            'team_leader': f"{developer.team.team_leader.user.first_name} {developer.team.team_leader.user.last_name}" if developer.team else "No team leader assigned",
            'project_name': project_name,
        })

    context = {
        'developers': developers_data,
        'team_leaders': team_leaders,
        'projects': projects,
        'selected_team_leader': selected_team_leader,
        'selected_project': selected_project,
        'pending_count': count,
        'project_count': pcount
    }
    return render(request, 'show_developers.html', context)









def teamleaderhome(request):    
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to view this page.')
        return redirect('loginpage')
    try:
        team_leader = Workers.objects.get(user=request.user)
    except Workers.DoesNotExist:
        messages.error(request, 'Team Leader profile not found.')
        return redirect('loginpage')

    today_report_submitted = DailyReportTeamLeader.objects.filter(
        team_leader=team_leader,
        report_date=date.today()
    ).exists()

    return render(request, 'sample.html', {
        'teamleader': team_leader,
        'today_report_submitted': today_report_submitted,
    })

def teamleaderprofile(request, sp):
    team_leader = get_object_or_404(Workers, id=sp)  
    worker = get_object_or_404(Workers, user=team_leader.user)
    assigned_projects = Project.objects.filter(worker=worker) 

    return render(request, 'teamleaderprofile.html', {
        'team_leader': team_leader,
        'worker': worker, 
        'assigned_projects': assigned_projects
    })

def teamleaderprofileedit(request,se):
    team_leader = get_object_or_404(Workers, id=se)  
    worker = get_object_or_404(Workers, user=team_leader.user)
    return render(request, 'teamleaderprofileedit.html', {
        'team_leader': team_leader,
        'worker': worker
    })

def update_teamleader(request, se):
    team_leader = get_object_or_404(Workers, id=se)
    u = team_leader.user  
    worker = team_leader  

    if request.method == 'POST':
        new_first_name = request.POST.get('fname')
        new_last_name = request.POST.get('lname')
        new_username = request.POST.get('uname')
        new_email = request.POST.get('mail')
        new_mobile = request.POST.get('phone')


        if User.objects.exclude(id=u.id).filter(username=new_username).exists():
            messages.error(request, "Username already exists.")
            return redirect('update_teamleader', se=se)

        if User.objects.exclude(id=u.id).filter(email=new_email).exists():
            messages.error(request, "Email must be unique.")
            return redirect('update_teamleader', se=se)

        if Workers.objects.exclude(id=worker.id).filter(mobile=new_mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('update_teamleader', se=se)

        if not re.match(r'.+@.+\..+', new_email):
            messages.error(request, "Email format is not correct.")
            return redirect('update_teamleader', se=se)

        u.first_name = new_first_name
        u.last_name = new_last_name
        u.username = new_username
        u.email = new_email
        u.save()

        worker.mobile = request.POST.get('phone')
        worker.address = request.POST.get('address')
        worker.department = request.POST.get('department')
        worker.course_completed = request.POST.get('course_completed')

        new_img = request.FILES.get('image')
        if new_img:
            if worker.image and os.path.isfile(worker.image.path):
                os.remove(worker.image.path)
            worker.image = new_img 
        
        worker.save()
        messages.success(request, "Team Leader profile updated successfully.")
        return redirect('teamleaderprofile', sp=team_leader.id)  

    return render(request, 'teamleaderprofileedit.html', {
        'team_leader': team_leader,
        'worker': worker
    })

def reset_password_team_leader(request):
    if request.method == 'POST':
        current_password = request.POST.get('cpassword')
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('confirm')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('reset_password_team_leader')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match with confirm password")
            return redirect('reset_password_team_leader')

        if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[@$!%*?&]', new_password):
            messages.error(request, 'Require minimum 8 charectors, at least 1 digit and 1 special character')
            return redirect('reset_password_team_leader')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Password has been reset successfully.")
        return redirect('reset_password_team_leader')
    return render(request, 'resetpasswordteamleader.html')

@login_required(login_url='homepage')
def view_assigned_projects(request):
    worker = Workers.objects.get(user=request.user)
    assigned_projects = Project.objects.filter(worker=worker)
    return render(request, 'assigned_projects.html', {
        'assigned_projects': assigned_projects
    })

@login_required
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.project_status != 'Ongoing':
        messages.error(request, "Project is not ongoing.")
        return redirect('view_assigned_projects') 

    assigned_work_count = Work.objects.filter(project=project).count()

    if assigned_work_count == 0:
        messages.error(request, "Cannot complete project: No work has been assigned to developers.")
        return redirect('view_assigned_projects')

    verified_work_count = Work.objects.filter(project=project, status='Verified').count()

    if verified_work_count < assigned_work_count:
        messages.error(request, "Cannot complete project: Not all work has been verified.")
        return redirect('view_assigned_projects') 

    project.project_status = 'Completed'
    project.save()
    messages.success(request, "Project has been marked as completed successfully.")
    return redirect('view_assigned_projects') 


# def view_assigned_developers(request):
#     try:
#         team_leader = Workers.objects.get(user=request.user)

#         assigned_developers = Python.objects.filter(
#             team__team_leader=team_leader,
#             role='Developer'
#         ).select_related('user')  

#         developer_name = request.GET.get('developer_name', '')

#         if developer_name:
#             assigned_developers = assigned_developers.filter(id=developer_name) 

#         workers_info = []
#         for developer in assigned_developers:
#             worker = Workers.objects.filter(user=developer.user).first()
#             workers_info.append((developer, worker))

#     except Workers.DoesNotExist:
#         team_leader = None
#         workers_info = []

#     return render(request, 'view_assigned_developers.html', {
#         'team_leader': team_leader,
#         'workers_info': workers_info,
#         'assigned_developers': assigned_developers, 
#     })

# def assign_work(request):
#     team_leader = get_object_or_404(Workers, user=request.user)
#     project = Project.objects.filter(worker=team_leader).first()
#     developers = Python.objects.filter(team__team_leader=team_leader)

#     if request.method == 'POST':
#         developer_id = request.POST.get('developer')
#         module_description = request.POST.get('module')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         if not developer_id or not module_description or not start_date or not end_date:
#             messages.error(request, "All fields are required.")
#         else:
#             developer = get_object_or_404(Python, id=developer_id)
#             work = Work.objects.create(
#                 developer=developer,
#                 project=project,
#                 team_leader=team_leader,
#                 module=module_description,
#                 start_date=start_date,
#                 end_date=end_date
#             )
#             work.save()
#             messages.success(request, "Work assigned successfully!")
#             return redirect('assign_work')

#     return render(request, 'assign_work.html', {
#         'project': project,
#         'developers': developers,
#     })

# def view_submitted_works(request):
#     team_leader = get_object_or_404(Workers, user=request.user)
#     submitted_works = Work.objects.filter(team_leader=team_leader, status='Submitted')
#     developers = Python.objects.filter(team__team_leader=team_leader).distinct()
#     projects = Project.objects.filter(worker=team_leader)  

#     developer_name = request.GET.get('developer_name', '')
#     project_name = request.GET.get('project_name', '')
#     start_date = request.GET.get('start_date', '')
#     end_date = request.GET.get('end_date', '')

#     if developer_name:
#         submitted_works = submitted_works.filter(developer__id=developer_name)

#     if project_name:
#         submitted_works = submitted_works.filter(project__id=project_name)  

#     if start_date:
#         submitted_works = submitted_works.filter(submit_date__gte=start_date)

#     if end_date:
#         submitted_works = submitted_works.filter(submit_date__lte=end_date)

#     for work in submitted_works:
#         if work.submit_date and work.end_date:
#             if work.submit_date > work.end_date:
#                 work.late_days = (work.submit_date - work.end_date).days
#             else:
#                 work.late_days = 0
#         else:
#             work.late_days = 0
#     return render(request, 'view_submitted_works.html', {
#         'submitted_works': submitted_works,
#         'developers': developers,
#         'projects': projects,
#     })

# def assign_work(request):
#     team_leader = get_object_or_404(Workers, user=request.user)
#     projects = Project.objects.filter(worker=team_leader)

#     if not projects.exists() or all(project.project_status == 'Completed' for project in projects):
#         messages.error(request, "No active project available")
#         return render(request, 'assign_work.html', {
#             'project': None,
#             'developers': [],
#         })

#     project = projects.exclude(project_status='Completed').first()
#     developers = Python.objects.filter(team__team_leader=team_leader)

#     if request.method == 'POST':
#         developer_id = request.POST.get('developer')
#         module_description = request.POST.get('module')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         if not developer_id or not module_description or not start_date or not end_date:
#             messages.error(request, "All fields are required.")
#         else:
#             developer = get_object_or_404(Python, id=developer_id)
#             work = Work.objects.create(
#                 developer=developer,
#                 project=project,
#                 team_leader=team_leader,
#                 module=module_description,
#                 start_date=start_date,
#                 end_date=end_date
#             )
#             messages.success(request, "Work assigned successfully!")
#             return redirect('assign_work')

#     return render(request, 'assign_work.html', {
#         'project': project,
#         'developers': developers,
#     })

def view_assigned_developers(request):
    try:
        team_leader = Workers.objects.get(user=request.user)

        assigned_developers = Python.objects.filter(
            team__team_leader=team_leader,
            role='Developer'
        ).select_related('user', 'team__project')

        developer_name = request.GET.get('developer_name', '')
        project_id = request.GET.get('project', '')

        if developer_name:
            assigned_developers = assigned_developers.filter(id=developer_name)

        if project_id:
            assigned_developers = assigned_developers.filter(team__project__id=project_id).distinct()

        workers_info = []
        for developer in assigned_developers:
            worker = Workers.objects.filter(user=developer.user).first()
            workers_info.append((developer, worker))

        projects = Project.objects.filter(team__team_leader=team_leader).distinct()

    except Workers.DoesNotExist:
        team_leader = None
        workers_info = []
        projects = []

    return render(request, 'view_assigned_developers.html', {
        'team_leader': team_leader,
        'workers_info': workers_info,
        'assigned_developers': assigned_developers,
        'projects': projects,
        'developer_name': developer_name,
        'project_id': project_id,
    })

def assign_work(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    projects = Project.objects.filter(worker=team_leader)

    if not projects.exists() or all(project.project_status == 'Completed' for project in projects):
        messages.error(request, "No active project available")
        return render(request, 'assign_work.html', {
            'project': None,
            'developers': [],
        })

    project = projects.exclude(project_status='Completed').first()
    developers = Python.objects.filter(team__project=project)

    if request.method == 'POST':
        developer_id = request.POST.get('developer')
        module_description = request.POST.get('module')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not developer_id or not module_description or not start_date or not end_date:
            messages.error(request, "All fields are required.")
        else:
            developer = get_object_or_404(Python, id=developer_id)
            work = Work.objects.create(
                developer=developer,
                project=project,
                team_leader=team_leader,
                module=module_description,
                start_date=start_date,
                end_date=end_date
            )
            messages.success(request, "Work assigned successfully!")
            return redirect('assign_work')

    return render(request, 'assign_work.html', {
        'project': project,
        'developers': developers,
    })

def view_submitted_works(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    
    submitted_works = Work.objects.filter(
        team_leader=team_leader
    ).exclude(status='Verified')

    developers = Python.objects.filter(team__team_leader=team_leader).distinct()

    developer_name = request.GET.get('developer_name', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if developer_name:
        submitted_works = submitted_works.filter(developer__id=developer_name)

    if status:
        if status == "Not Submitted":
            submitted_works = submitted_works.filter(submit_date__isnull=True)
        else:
            submitted_works = submitted_works.filter(status=status)

    if start_date:
        submitted_works = submitted_works.filter(submit_date__gte=start_date)

    if end_date:
        submitted_works = submitted_works.filter(submit_date__lte=end_date)

    for work in submitted_works:
        if work.submit_date and work.end_date:
            if work.submit_date > work.end_date:
                work.late_days = (work.submit_date - work.end_date).days
            else:
                work.late_days = 0
        else:
            work.late_days = 0

    return render(request, 'view_submitted_works.html', {
        'submitted_works': submitted_works,
        'developers': developers,
    })


def verify_work(request, work_id):
    work = get_object_or_404(Work, id=work_id)    
    work.status = 'Verified'
    work.save()
    messages.success(request, 'Work has been verified successfully.')
    return redirect('view_submitted_works')

@login_required
def view_verified_works(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    
    projects = Project.objects.filter(team__team_leader=team_leader).distinct()
    verified_works = Work.objects.filter(team_leader=team_leader, status='Verified')
    developers = Python.objects.filter(team__team_leader=team_leader).distinct()
    
    developer_name = request.GET.get('developer_name', '')
    project_id = request.GET.get('project')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if developer_name:
        verified_works = verified_works.filter(developer__id=developer_name)

    if project_id:
        verified_works = verified_works.filter(project__id=project_id)

    if start_date:
        verified_works = verified_works.filter(submit_date__gte=start_date)
    if end_date:
        verified_works = verified_works.filter(submit_date__lte=end_date)

    return render(request, 'view_verified_works.html', {
        'verified_works': verified_works,
        'developers': developers,
        'projects': projects,
        'developer_name': developer_name,
        'project_id': project_id,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def view_developer_reports(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    teams = Team.objects.filter(team_leader=team_leader)
    developers = Python.objects.filter(team__in=teams)
    selected_developer = request.GET.get('developer')
    selected_project = request.GET.get('project')
    daily_reports = DailyReport.objects.filter(developer__in=developers).order_by('-report_date')
    if selected_developer:
        daily_reports = daily_reports.filter(developer__id=selected_developer)
    if selected_project:
        daily_reports = daily_reports.filter(project__id=selected_project)
    project_ids = daily_reports.values_list('project', flat=True).distinct()
    projects = Project.objects.filter(id__in=project_ids)

    return render(request, 'view_developer_reports.html', {
        'daily_reports': daily_reports,
        'developers': developers,
        'projects': projects,
        'selected_developer': selected_developer,
        'selected_project': selected_project,
    })

# def update_daily_report_teamleader(request):
#     team_leader = get_object_or_404(Workers, user=request.user)
#     today_report = DailyReportTeamLeader.objects.filter(
#         team_leader=team_leader,
#         report_date=date.today()
#     ).first()

#     projects = Project.objects.filter(team__team_leader=team_leader).distinct()

#     if request.method == 'POST':
#         if today_report:
#             messages.error(request, "You have already submitted a report for today.")
#             return redirect('update_daily_report_teamleader')

#         description = request.POST.get('description')
#         report_file = request.FILES.get('work_report')
#         project_id = request.POST.get('project_id')
#         project = get_object_or_404(Project, id=project_id)
#         report = DailyReportTeamLeader(
#             team_leader=team_leader,
#             project=project,
#             description=description,
#             work_report=report_file if report_file else None,
#             report_status='Submitted',
#             report_date=timezone.now()
#         )
#         report.save()

#         messages.success(request, "Daily report submitted successfully!")
#         return redirect('update_daily_report_teamleader')
#     return render(request, 'update_daily_report_teamleader.html', {
#         'today_report': today_report,
#         'projects': projects,
#     })


def update_daily_report_teamleader(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    today = date.today()
    
    projects = Project.objects.filter(
        team__team_leader=team_leader,
        project_status='ongoing'
    ).distinct()

    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        existing_report = DailyReportTeamLeader.objects.filter(
            team_leader=team_leader,
            project=project,
            report_date=today
        ).first()

        if existing_report:
            messages.error(request, "You have already submitted a report for this project today.")
            return redirect('update_daily_report_teamleader')

        description = request.POST.get('description')
        report_file = request.FILES.get('work_report')
        
        report = DailyReportTeamLeader(
            team_leader=team_leader,
            project=project,
            description=description,
            work_report=report_file if report_file else None,
            report_status='Submitted',
            report_date=today  
        )
        report.save()

        messages.success(request, "Daily report submitted successfully!")
        return redirect('update_daily_report_teamleader')

    return render(request, 'update_daily_report_teamleader.html', {
        'projects': projects,
    })

@login_required
def view_teamleaders_daily_reports(request):
    team_leader = get_object_or_404(Workers, user=request.user)
    
    projects = Project.objects.filter(team__team_leader=team_leader).distinct()
    reports = DailyReportTeamLeader.objects.filter(team_leader=team_leader).order_by('report_date')

    project_id = request.GET.get('project')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if project_id:
        reports = reports.filter(project__id=project_id)
    
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        reports = reports.filter(report_date__range=(start_date, end_date))

    return render(request, 'view_teamleaders_daily_reports.html', {
        'reports': reports,
        'projects': projects,
        'project_id': project_id,
        'start_date': start_date,
        'end_date': end_date,
    })






















    

def developerhome(request):
    developer = request.user.python_set.first()  
    if not developer:
        messages.error(request, 'Developer profile not found.')
        return redirect('loginpage')
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    return render(request, 'developerhome.html', {
        'developer': developer,
        'today_report_submitted': today_report,'pending_works_count': pending_works_count
    })

def developerprofile(request, dp):
    developer = get_object_or_404(Python, id=dp)
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    worker = get_object_or_404(Workers, user=developer.user)
    assigned_projects = Project.objects.filter(worker=worker)

    return render(request, 'developerprofile.html', {
        'developer': developer,
        'worker': worker,
        'assigned_projects': assigned_projects,'today_report_submitted': today_report,'pending_works_count': pending_works_count
    })

def developereditprofile(request, dp):
    developer = get_object_or_404(Python, id=dp)   
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    worker = get_object_or_404(Workers, user=developer.user)
    return render(request, 'developereditprofile.html', {
        'developer': developer,
        'worker': worker,'today_report_submitted': today_report,'pending_works_count': pending_works_count
    })

def update_developer(request, dp):
    developer = get_object_or_404(Python, id=dp)
    u = developer.user  
    worker = get_object_or_404(Workers, user=u)  

    if request.method == 'POST':
        new_first_name = request.POST.get('fname')
        new_last_name = request.POST.get('lname')
        new_username = request.POST.get('uname')
        new_email = request.POST.get('mail')
        new_mobile = request.POST.get('phone')


        if User.objects.exclude(id=u.id).filter(username=new_username).exists():
            messages.error(request, "Username already exists.")
            return redirect('developereditprofile', dp=dp)

        if User.objects.exclude(id=u.id).filter(email=new_email).exists():
            messages.error(request, "Email must be unique.")
            return redirect('developereditprofile', dp=dp)
        
        if Workers.objects.exclude(id=worker.id).filter(mobile=new_mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('developereditprofile', dp=dp)

        if not re.match(r'.+@.+\..+', new_email):
            messages.error(request, "Email format is not correct")
            return redirect('developereditprofile', dp=dp)

        u.first_name = new_first_name
        u.last_name = new_last_name
        u.username = new_username
        u.email = new_email
        u.save()

        worker.mobile = request.POST.get('phone')
        worker.address = request.POST.get('address')
        worker.department = request.POST.get('department')
        worker.course_completed = request.POST.get('course_completed')

        new_img = request.FILES.get('image')
        if new_img:
            if worker.image and os.path.isfile(worker.image.path):
                os.remove(worker.image.path) 
            worker.image = new_img  
        
        worker.save() 

        messages.success(request, "Developer profile updated successfully.")
        return redirect('developerprofile', dp=developer.id)  

    return render(request, 'developerprofileedit.html', {
        'developer': developer,
        'worker': worker
    })

def reset_password_developer(request):
    if request.method == 'POST':
        current_password = request.POST.get('cpassword')
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('confirm')

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('reset_password_developer')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match with confirm password.")
            return redirect('reset_password_developer')

        if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[@$!%*?&]', new_password):
            messages.error(request, 'Require minimum 8 characters, at least 1 digit, and 1 special character.')
            return redirect('reset_password_developer')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Password has been reset successfully.")
        return redirect('reset_password_developer')
    return render(request, 'resetpassworddeveloper.html')

def assigned_project_for_developer(request):
    user = request.user  
    developer = get_object_or_404(Python, user=user)  
    team = Team.objects.filter(python=developer).first()

    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    if team:
        project = team.project 
        team_leader = team.team_leader  
    else:
        project = None
        team_leader = None 
    return render(request, 'assigned_project_for_developer.html', {
        'developer': developer,
        'project': project,  
        'team_leader': team_leader,
        'today_report_submitted': today_report,'pending_works_count': pending_works_count
    })

def view_team_leader_details(request, developer_id):
    developer = get_object_or_404(Python, id=developer_id)
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    team = developer.team
    team_leader = team.team_leader if team else None
    project = team_leader.project_set.first() if team_leader else None
    return render(request, 'team_leader_details.html', {
        'developer': developer,
        'team_leader': team_leader,
        'project': project,
        'today_report_submitted': today_report,'pending_works_count': pending_works_count
    })

def view_assigned_work(request):
    developer = get_object_or_404(Python, user=request.user)
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    assigned_works = Work.objects.filter(developer=developer, status='Pending')

    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        uploaded_file = request.FILES.get('upload')
        work = get_object_or_404(Work, id=work_id)
        work.upload = uploaded_file
        work.submit_date = date.today()
        if work.submit_date > work.end_date:
            late_days = (work.submit_date - work.end_date).days
            messages.warning(request, f"Submission is late by {late_days} days.")
        else:
            messages.success(request, "Work submitted successfully!")

        work.status = 'Submitted'
        work.save()

        return redirect('view_assigned_work')

    return render(request, 'view_assigned_work.html', {
        'assigned_works': assigned_works,'today_report_submitted': today_report,'pending_works_count': pending_works_count

    })


@login_required
def view_submitted_works_by_developer(request):
    developer = get_object_or_404(Python, user=request.user)
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()
    
    projects = Project.objects.filter(team__python=developer).distinct()
    submitted_works = Work.objects.filter(developer=developer, submit_date__isnull=False)
    
    project_id = request.GET.get('project')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    
    if project_id:
        submitted_works = submitted_works.filter(project__id=project_id)
    
    if start_date and end_date:
        parsed_start = parse_date(start_date)
        parsed_end = parse_date(end_date)
        if parsed_start > parsed_end:
            messages.error(request, "Start date cannot be greater than end date.")
        else:
            submitted_works = submitted_works.filter(submit_date__range=(start_date, end_date))
    elif start_date:
        submitted_works = submitted_works.filter(submit_date__gte=start_date)
    elif end_date:
        submitted_works = submitted_works.filter(submit_date__lte=end_date)
    
    if status:
        submitted_works = submitted_works.filter(status=status)

    return render(request, 'view_submitted_works_by_developer.html', {
        'submitted_works': submitted_works,
        'projects': projects,
        'project_id': project_id,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'today_report_submitted': today_report,
        'pending_works_count': pending_works_count
    })

def update_daily_report(request):
    developer = get_object_or_404(Python, user=request.user)
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).first()
    projects = Project.objects.filter(team__python=developer).distinct()

    if request.method == 'POST':
        if today_report:
            messages.warning(request, "You have already submitted a daily report for today.")
            return redirect('update_daily_report')  
        description = request.POST.get('description')
        report_file = request.FILES.get('report_file')
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        team = get_object_or_404(Team, project=project)  
        team_leader = team.team_leader
        report = DailyReport(
            developer=developer,
            project=project, 
            team_leader=team_leader, 
            report_date=date.today(),
            description=description,
            work_report=report_file, 
            report_status='Submitted',
        )
        report.save()
        messages.success(request, "Daily report submitted successfully!")
        return redirect('update_daily_report') 
    return render(request, 'update_daily_report.html', {
        'today_report': today_report,
        'projects': projects,
        'pending_works_count': pending_works_count

    })

def get_team_leader(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    team = project.team_set.first() 
    if team and team.team_leader:
        team_leader_name = f"{team.team_leader.user.first_name} {team.team_leader.user.last_name}"
    else:
        team_leader_name = 'No team leader assigned'

    return JsonResponse({'team_leader': team_leader_name})

@login_required
def view_daily_reports(request):
    developer = request.user.python_set.first()
    if not developer:
        messages.error(request, 'Developer profile not found.')
        return redirect('loginpage')

    projects = Project.objects.filter(team__python=developer).distinct()
    
    daily_reports = DailyReport.objects.filter(developer=developer).order_by('report_date')
    
    project_id = request.GET.get('project')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if project_id:
        daily_reports = daily_reports.filter(project__id=project_id)
    
    start_date = parse_date(start_date) if start_date else None
    end_date = parse_date(end_date) if end_date else None
    if start_date and end_date and start_date > end_date:
        messages.error(request, 'Start date cannot be greater than end date.')
    else:
        if start_date:
            daily_reports = daily_reports.filter(report_date__gte=start_date)
        if end_date:
            daily_reports = daily_reports.filter(report_date__lte=end_date)
    
    today_report = DailyReport.objects.filter(developer=developer, report_date=date.today()).exists()
    pending_works_count = Work.objects.filter(developer=developer, status='Pending').count()

    return render(request, 'view_daily_reports.html', {
        'daily_reports': daily_reports,
        'projects': projects,
        'project_id': project_id,
        'start_date': start_date,
        'end_date': end_date,
        'today_report_submitted': today_report,
        'pending_works_count': pending_works_count,
    })