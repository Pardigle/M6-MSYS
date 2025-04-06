from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account 

# Create your views here.
global message
global current_user
message = None
current_user = None

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes':dish_objects})

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})

def basic_list(request, pk):
    dish_objects = Dish.objects.all()
    user = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/basic_list.html', {'dishes':dish_objects, 'user':user})

def manage_account(request, pk):
    if(request.method=="POST"):
        button = request.POST.get("button")

        if button == "change_password":
            return redirect('change_password', pk=pk)

        elif button == "delete_account":
            return redirect('delete_account', pk=pk)

        elif button == "back":
            return redirect('basic_list', pk=pk)
    
    else:
        user = get_object_or_404(Account, pk=pk)
        return render(request, 'tapasapp/manage_account.html', {'user':user})
    
def change_password(request, pk):
    if(request.method=="POST"):
        button = request.POST.get("button")

        if button == "confirm":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')

            if new_password == new_password2:
                if old_password == Account.objects.get(pk=pk).getPassword():
                    Account.objects.filter(pk=pk).update(password=new_password)
                    return redirect('manage_account', pk=pk)
                
                else:
                    message = "Input correct old password. Try again."
                    return render(request, 'tapasapp/change_password.html', {'message':message})
            
            else:
                message = "Unmatching passwords. Try again."
                return render(request, 'tapasapp/change_password.html', {'message':message})
        
        elif button == "cancel":
            return redirect('manage_account', pk=pk)
    
    else:
        return render(request, 'tapasapp/change_password.html')

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('login')

def login(request):
    if(request.method=="POST"):
        button = request.POST.get("button")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if button == "login":
            valid_account = Account.objects.filter(username=username).exists()
            if valid_account:
                credentials = Account.objects.get(username=username)
                if password == credentials.getPassword():
                    global current_user
                    current_user = credentials
                    return redirect('basic_list', pk=current_user.pk)
                else:
                    return render(request, 'tapasapp/login.html', {'message': 'Incorrect password.'})
            else:
                return render(request, 'tapasapp/login.html', {'message': 'Account does not exist.'})
        
        elif button == "signup":
            return redirect('signup')
        
    else:
        global message
        return render(request, 'tapasapp/login.html', {'message':message})
        

def signup(request):
    if(request.method=="POST"):
        button = request.POST.get("button")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if button == "signup":
            username_exists = Account.objects.filter(username=username).exists()

            if not username_exists:
                Account.objects.create(username=username, password=password)
                global message
                message = 'Account created successfully.'
                return redirect('login')
            else:
                return render(request, 'tapasapp/signup.html', {'message':'Username is already taken.'})
            
        elif button == "login":
            return redirect('login')
        
    else:
        return render(request, 'tapasapp/signup.html')