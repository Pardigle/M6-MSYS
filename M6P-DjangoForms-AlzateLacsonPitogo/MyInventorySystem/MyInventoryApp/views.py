from django.shortcuts import render, redirect, get_object_or_404
from .models import WaterBottle, Supplier, Account

# Create your views here.

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
                    return redirect('view_supplier')
                else:
                    return render(request, 'MyInventoryApp/login.html', {'message': 'Incorrect password.'})
            else:
                return render(request, 'MyInventoryApp/login.html', {'message': 'Account does not exist.'})
    else:
        message = request.session.pop('message', None)
        fusername = request.session.pop('fresh_username', None)
        return render(request, 'MyInventoryApp/login.html', {'message':message, 'fusername':fusername})
    
def signup(request):
    if(request.method=="POST"):
        button = request.POST.get("button")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if button == "signup":
            username_exists = Account.objects.filter(username=username).exists()

            if not username_exists:
                Account.objects.create(username=username, password=password)
                request.session['message'] = 'Account created successfully.'
                request.session['fresh_username'] = username
                return redirect('login')
            else:
                return render(request, 'MyInventoryApp/signup.html', {'message':'Username is already taken.'})
        
    else:
        return render(request, 'MyInventoryApp/signup.html')

def view_bottles(request):
    bottle_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles':bottle_objects})

def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'supplier':supplier_objects})

def add_bottle(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/add_bottle.html', {'supplier':supplier_objects})