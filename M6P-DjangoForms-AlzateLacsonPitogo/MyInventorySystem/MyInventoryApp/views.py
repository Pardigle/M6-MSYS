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

def view_bottles(request, supplier_id):
    global current_user
    if current_user:
        supplier = get_object_or_404(Supplier, id=supplier_id)
        bottle_objects = WaterBottle.objects.filter(supplier=supplier)
        return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottle_objects, 'supplier': supplier})
    else:
        return redirect('login')

def view_bottle_details(request, pk):
    global current_user
    if current_user:
        bottle = get_object_or_404(WaterBottle, id=pk)
        return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle})
    else:
        return redirect('login')

def delete_bottle(request, bottle_id):
    global current_user
    if current_user:
        bottle = get_object_or_404(WaterBottle, id=bottle_id)
        supplier_id = bottle.supplier.id
        bottle.delete()
        return redirect('view_bottles', supplier_id=supplier_id)
    else:
        return redirect('login')

def view_supplier(request):
    global current_user
    if current_user:
        supplier_objects = Supplier.objects.all()
        return render(request, 'MyInventoryApp/view_supplier.html', {'supplier':supplier_objects})
    else:
        return redirect('login')

def add_bottle(request):
    global current_user
    if current_user:
        supplier_objects = Supplier.objects.all()
        return render(request, 'MyInventoryApp/add_bottle.html', {'supplier':supplier_objects})
    else:
        return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('login')

'''
Put this so that the log-in is required for every view.


    global current_user
    if current_user:
        <Your code>
    else:
        return redirect('login')

'''
