from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account 

# Create your views here.


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
    
def login(request):
    if(request.method=="POST"):
        button = request.POST.get("button")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if button == "login":
            if Account.objects.filter(username=username).exists():
                credentials = Account.objects.get(username=username)
                if password == credentials.getPassword():
                    return redirect('better_menu')
                else:
                    return render(request, 'tapasapp/login.html', {'error': 'Incorrect password.'})
            else:
                return render(request, 'tapasapp/login.html', {'error': 'Account does not exist.'})
        
        elif button == "signup":
            return redirect('signup')
        

    else:
        return render(request, 'tapasapp/login.html')
        

def signup(request):
    if(request.method=="POST"):
        button = request.POST.get("button")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if button == "signup":
            check_username = len(Account.objects.filter(username=username))

            if check_username == 0:
                Account.objects.create(username=username, password=password)
                return redirect('login')
            else:
                return render(request, 'tapasapp/signup.html', {'error':'Username is already taken.'})
            
        elif button == "login":
            return redirect('login')
        
    else:
        return render(request, 'tapasapp/signup.html')