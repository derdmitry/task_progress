from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import Target
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .forms import TargetForm, AddProgressForm, UserForm
from django.views import generic
from django.forms.models import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    message = 'Первая страница'
    return render(request, 'index.html', locals())

@login_required
def progress(request):
    from datetime import date
    current_date = date.today()
    message = 'Здесь будет прогресс -2'
    result = "непонятно"

    qs = Target.objects.filter(user=request.user.id).order_by('priority')

    #qs = Target.objects.order_by('priority')

    if request.method == 'POST':
        task_id = request.POST.get('id')
        new_progress = request.POST.get('new_progress')

        instances = Target.objects.filter(pk=task_id)
        instance = instances[0]
        instance.done = new_progress
        instance.save()

    return render(request, 'progress.html', locals())





def edit_target(request, id):
    targets = Target.objects.filter(pk=id)  # ищем нужную запись по id
    target = targets[0]  # она должна существовать
    if request.method == 'POST':
        form = TargetForm(request.POST, instance=target)  # и передаем ее в instance
        if form.is_valid():
            # task.archive = 'yes'
            form.save(commit=True)
            return redirect('progress')  # удобная функция из django.shortcuts
            # return render(request, 'list2.html', locals())
        else:
            message = "Ошибка"
            return render(request, 'error_page.html', locals())
    else:
        form = TargetForm(instance=target)

    return render(request, 'edit_target.html', {'form': form})


def edit_progress(request, id):
    targets = Target.objects.filter(pk=id)  # ищем нужную запись по id
    target = targets[0]  # она должна существовать
    if request.method == 'POST':
        form = AddProgressForm(request.POST, instance=target)  # и передаем ее в instance
        if form.is_valid():
            # task.archive = 'yes'
            form.save(commit=True)
            return redirect('show')  # удобная функция из django.shortcuts
            # return render(request, 'edit_progress.html', {'form': form})
        else:
            message = "Ошибка"
            return render(request, 'error_page.html', locals())
    else:
        form = AddProgressForm(instance=target)

    return render(request, 'edit_progress.html', {'form': form})


def delete_target(request, id):
    targets = Target.objects.filter(pk=id)  # ищем нужную запись по id
    target = targets[0]  # она должна существовать
    if request.method == 'POST':
        form = TargetForm(request.POST, instance=target)  # и передаем ее в instance
        if form.is_valid():
            target.delete()
            # form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Цели больше нет")
            return redirect('progress')  # удобная функция из django.shortcuts
            # return render(request, 'list2.html', locals())
        else:
            message = "Ошибка"
            return render(request, 'error_page.html', locals())
    else:
        form = TargetForm(instance=target)

    return render(request, 'delete_target.html', {'form': form})


#_____registration__________________

def register(request):
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            # print(user_form.errors)
            # !обработать неправильный ввод!
            message = user_form.errors
            return render(request, 'error_page.html', locals())

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'registered': registered} )


#________login_____________

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('progress')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Ваш аккунт не активен")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Неправильный логин или пароль!") #Обработать
            message = "Неправильный логин или пароль!"
            return render(request, 'error_page.html', locals())
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})

#__________logout________________

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect('login')



@login_required
def add_target(request):
    # добавить новую цель
    posted_ok = False
    if request.method == 'POST':
        form = TargetForm(request.POST)

        if form.is_valid():

            new_item = form.save(commit=False)
            new_item.user_id = request.user.id #добвавление id пользователя
            #new_item.user_id= 1288
            new_item.save()
            posted_ok = True
            return render(request, 'add_target.html', locals())
        else:
            # The supplied form contained errors - just print them to the terminal.
            message = "Ошибка"
            return render(request, 'error_page.html', locals())
    else:
        # If the request was not a POST, display the form to enter details.
        form = TargetForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_target.html', locals())



# мои пробы

def trial(request):
    from datetime import date
    current_date = date.today()
    message = 'Здесь будет прогресс'

    AddProgressFormset = modelformset_factory(Target, fields=('done',), extra=0, )
    qs = Target.objects.order_by('priority')
    if request.method == "POST":
        # qs = Target.objects.order_by('priority')
        formset = AddProgressFormset(request.POST, request.FILES,
                                     queryset=qs)
        if formset.is_valid():
            formset.save()
            return redirect('show')
            #return render(request, 'show.html')
    else:
        # qs = Target.objects.order_by('priority')
        formset = AddProgressFormset(queryset=qs)

    data = []

    for i in range(len(qs)):
        data.append([qs[i],formset[i]])

    return render(request, 'show.html', {'formset': formset,
                                          'current_date': current_date,
                                          'data': data,
                                         }

                  )


def show(request):
    # gjrfpfnm ghjuhtcc
    from datetime import date
    current_date = date.today()
    message = 'Здесь будет прогресс'

    qs = Target.objects.order_by('priority')
    add_progress_form = AddProgressForm()

    return render(request, 'show.html', locals())




