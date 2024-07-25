from django.shortcuts import render, redirect, get_object_or_404
from .forms import MoneyForm, MoneySearch, EditTodoForm, IsActive, AddTitleForm, UserLoginForm
from .forms import  TodoTitleForm, UserRegisterForm, EmailForm
from .models import Money, TodoList, TitleTodo, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils.timezone import make_aware
from datetime import datetime, date, timedelta
from .matplotlib_view import generate_plot, generate_pie, generate_pie_task
from django.utils.timezone import timezone
import calendar
from django.contrib.auth import login as auth_login, authenticate , get_user_model, logout
from django.http import HttpResponse
from Google import create_message, send_message, sending_message
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes







def home(request):
    if request.user.is_authenticated:
        return redirect('todolist:dashboard')
    
    return render(request, 'home.html')


def dashboard(request):

    return render(request, 'dashboard.html')



def login_view(request):
    user_form = UserLoginForm()
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('todolist:home')
            else:
                user_form.add_error(None, 'Failed to login')
    context = {
        'user_form' : user_form
    }

    return render(request,'login.html', context)


def register_view(request):
    register_form = UserRegisterForm()
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            password = register_form.cleaned_data['password1']
            user = authenticate(email=user.email, password=password)
            if user is not None:
                auth_login(request, user)
            return redirect('todolist:register_completed')
    context = {
        'register_form' : register_form
    }
    return render(request, 'registration/register.html', context)


def register_completed(request):
    if not request.user.is_authenticated:
        return redirect('todolist:home')
    elif request.user.is_active == True:
        return redirect('todolist:dashboard')
    elif request.user.is_active == False:
        return render(request, 'registration/register_completed.html')
    

#TODO display the user email after reset password is sent
def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


#TODO Refactor this function to utils.py
def password_reset(request):
    email_form = EmailForm()
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        email = request.POST['email']
        user_email = User.objects.filter(email=email)
        if user_email.exists():
            for user in user_email:
                sender = settings.DEFAULT_FROM_EMAIL
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f'{settings.SITE_URL}/reset_password_email/{uid}/{token}/'
                message = f'Hello dear {user.username}'
                f'here is your link to reset your password'
                f'\n {reset_url}'
                to = user.email
                subject = 'Reset Password'
                sending_message(
                    sender,
                    to,
                    subject,
                    message
                )
        return redirect("todolist:password_reset_done")
    return render(request, "registration/password_reset_form.html", {'email_form' : email_form})


def logout_view(request):
    logout(request)
    return redirect('todolist:home')


def activation_user(request, token):
    User = get_user_model()
    user = get_object_or_404(User, activation_token=token)
    if user.is_active:
        return render(request, 'registration/activated_user.html' , {'user' : user})
    user.is_active = True
    user.save()
    return render(request, 'registration/activated_user.html', {'user' : user})


def profile(request):
    return render(request,'profile.html')


def profile_settings(request):
    return render(request, 'profile_settings.html')

#TODO ADD JAVASCRIPT TO SHOW THE MATPLOTLIB FILES
#TODO ADD SIGNAL TO ADD NEW NOTE EVERY TIME USER DELETE ALL NOTES SO MATPLOTLIB WORK
@login_required()
def todo_view(request, user_id):
    #filtering the todolist from user_id
    todolist = TodoList.objects.filter(user_id=user_id)
    titles = TitleTodo.objects.filter(todolist__user_id=user_id).distinct()
    title_task_map = {}
    for title in titles:
        task = todolist.filter(title=title)
        title_task_map[title] = task
    #showing current month 
    month = datetime.now().strftime('%B')  
    #Making the start day and the end day of the month
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(day=1, month=today.month % 12 + 1) - timedelta(days=1)
    #Taking tasks created this month
    tasks_this_month = todolist.filter(created_at__gte=start_of_month, created_at__lte=end_of_month)
    tasks_this_month_count = tasks_this_month.count()
    #Taking tasks completed this month
    tasks_completed_this_month = todolist.filter(created_at__gte=start_of_month, created_at__lte=end_of_month, active=False)
    tasks_completed_this_month_count = tasks_completed_this_month.count()
    #Overal tasks
    overall_tasks = todolist.count()
    overall_tasks_completed = todolist.filter(active= False).count()
    #taking the important task
    important_tasks = todolist.filter(important=True)

    '''matplotlib'''
    #Chart about how many tasks did user completed each day
    #First value : month range
    num_days = calendar.monthrange(today.year, today.month)[1] 
    #Second value : task completed each day
    #Wrapped it into for iiteration to iterate over every single day of month and see
    #how many task each day were completed
    task_count = []
    for day in range(1, num_days +1):
        start_of_day = datetime(today.year, today.month, day, 0, 0, 0, tzinfo=timezone.utc)
        end_of_day = datetime(today.year, today.month, day, 23, 59, 59, tzinfo=timezone.utc)
        active_changes = todolist.filter(
            active=False,
            updated_at__gte = start_of_day,
            updated_at__lte = end_of_day,

        ).count()
        task_count.append(active_changes)
    plot_path = generate_plot(range(1,num_days+1),
                               task_count,
                                 'Tasks completed',
                                 '',
                                 'Days','Tasks')
    #generating plt_pie from matplotlib_view.py
    active = todolist.filter(active=True).count()
    not_active = todolist.filter(active=False).count()
    plot_path_pie = generate_pie(active, not_active)
    #generating plt_pie_task from matplotlib_view.py
    title_task_count = []
    for title in titles:
        count = todolist.filter(title=title).count()
        title_task_count.append(count)
    plot_path_pie_task = generate_pie_task(title_task_count, titles)

    context = {
        'title_task_map' : title_task_map,
        'month' : month,
        'todolist' : todolist,
        'tasks_this_month' : tasks_this_month,
        'tasks_this_month_count' : tasks_this_month_count,
        'tasks_completed_this_month' : tasks_completed_this_month,
        'tasks_completed_this_month_count' : tasks_completed_this_month_count,
        'overall_tasks' : overall_tasks,
        'overall_tasks_completed' : overall_tasks_completed,
        'important_tasks' : important_tasks,
        'titles' : titles,
        'plot_path' : plot_path,
        'plot_path_pie' : plot_path_pie,
        'plot_path_pie_task' : plot_path_pie_task,

    }
    return render(request,'todo_view.html', context)

def add_title_todo(request, user_id):
    form = TodoTitleForm()
    if request.method == 'POST':
        form = TodoTitleForm(request.POST, user=request.user)
        if form.is_valid():
            title_form = form.save(commit=False)
            title_form.user = request.user
            title_form.save()
            return redirect('todolist:todo_view', user_id)
    context = { 
        'form': form
    }
    return render(request, 'add_todo_title.html', context)



def add_todo_with_title(request, user_id):
    form = EditTodoForm()
    add_title = AddTitleForm(user=request.user)
    if request.method == 'POST':
        form = EditTodoForm(data=request.POST)
        add_title = AddTitleForm(data=request.POST, user=request.user)
        if form.is_valid() and add_title.is_valid() :
            title_instance = add_title.cleaned_data['title']
            todo_instance = form.save(commit=False)
            todo_instance.user = request.user
            todo_instance.title = title_instance
            todo_instance.save()
            return redirect('todolist:todo_view', user_id =user_id)
    context = {
        'form' : form,
        'add_title' : add_title
    }
    return render(request,'add_todo_with_title.html', context)


def edit_task(request, user_id, todolist_id):
    task = get_object_or_404(TodoList, id=todolist_id)
    form = EditTodoForm(instance=task)
    is_active = IsActive(instance=task)
    if request.method == 'POST':
        form = EditTodoForm(instance=task, data=request.POST)
        is_active = IsActive(instance=task, data=request.POST)
        if form.is_valid() and is_active.is_valid():
            form.save()
            is_active.save()
            return redirect('todolist:todo_view', user_id = user_id)
    context = {
        'form' : form,
        'task' : task,
        'is_active' : is_active
    }
    return render(request, 'edit_task.html', context)


def delete_task(request, user_id, todolist_id):
    task = get_object_or_404(TodoList, id=todolist_id)
    if request.method == "POST":
        task.delete()
        return redirect('todolist:todo_view',user_id)
    context = {
        'task' : task,
        
    }
    return render(request, 'delete_task.html', context )


def edit_current_task(request, user_id,title_id,):
    form = EditTodoForm()
    title_instance = get_object_or_404(TitleTodo, pk =title_id)
    if request.method == 'POST':
        form = EditTodoForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.title = title_instance
            new_task.user = request.user
            new_task.save()

            return redirect('todolist:todo_view', user_id=user_id)
    context ={
        'form' : form,
        'user_id' : user_id,
        'title_id' : title_id
    }
    return render(request, 'edit_current_task.html', context)


def set_completed(request, user_id, todolist_id):
    task = get_object_or_404(TodoList, id=todolist_id)
    if request.method == 'POST':
        task.active = False
        task.save()
        return redirect('todolist:todo_view', user_id)
    
    context = {
        'task': task
    }
    return render(request, 'set_completed.html', context)


@login_required(login_url='todolist:home')
def money_view(request):
    form = MoneySearch(request.GET)
    money_object = Money.objects.all()
    search_query = request.GET.get('search_query')
    important_only = request.GET.get('important_only')
    if search_query:
        money_object = money_object.filter(

            Q(field_info__icontains=search_query) |
            Q(what_info__icontains=search_query) |
            Q(type_info__icontains=search_query) |
            Q(created_at__icontains=search_query) |
            Q(money_info__icontains=search_query) 

        )
    if important_only:
        money_object = money_object.filter(
            important_info=True
        )

    results_per_page = request.GET.get('results_per_page', 10)
    paginator = Paginator(money_object, results_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    context = {
        'results_per_page' : results_per_page,
        'page_obj' : page_obj,
        'form' : form,
        'search_query' : search_query
    }
    return render(request,'money_view.html', context)



def money_view_add(request):
    form = MoneyForm()
    if request.method == 'POST':
        form = MoneyForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('todolist:money_view')
    context = {
        'form' : form
    }
    return render(request, 'money_view_add.html', context)
