from django.shortcuts import render, redirect, get_object_or_404
from .models import WaterBottle, Supplier, Account

# Create your views here.
global current_user
global message
message = None
current_user = None

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
                    request.session['account_id'] = credentials.pk
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
    global current_user
    if current_user:
        # Show all bottles in the system
        bottles = WaterBottle.objects.all()
        return render(request, 'MyInventoryApp/view_bottles.html', {
            'bottles': bottles,
            'user':current_user
        })
    else:
        return redirect('login')

def view_bottle_details(request, pk):
    global current_user
    if current_user:
        bottle = get_object_or_404(WaterBottle, pk=pk)

        # Handle the Delete button
        if request.method == "POST" and "delete" in request.POST:
            bottle.delete()
            return redirect("view_bottles")

        # Otherwise just render the details page
        return render(request, "MyInventoryApp/view_bottle_details.html", {
            "bottle": bottle,
            "user":current_user
        })
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
        return render(request, 'MyInventoryApp/view_supplier.html', {'supplier':supplier_objects, 'user':current_user})
    else:
        return redirect('login')

def add_bottle(request):
    global current_user
    if current_user:
        if request.method == 'POST':

            sku = request.POST.get('sku')
            brand = request.POST.get('brand')
            cost = request.POST.get('cost')
            size = request.POST.get('size')
            mouth_size = request.POST.get('mouth_size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            supplier_id = request.POST.get('supplier')

            if not all([sku, brand, cost, size, mouth_size, color, quantity, supplier_id]):
                return render(request, 'MyInventoryApp/add_bottle.html', {
                    'supplier': Supplier.objects.all(),
                    'message': 'Please fill out all fields before confirming.'
                })

            if WaterBottle.objects.filter(sku=sku).exists():
                    return render(request, 'MyInventoryApp/add_bottle.html', {
                        'supplier': Supplier.objects.all(),
                        'message': 'A bottle with this SKU already exists.'
                    })
                
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                return render(request, 'MyInventoryApp/add_bottle.html', {
                    'supplier': Supplier.objects.all(),
                    'message': 'Selected supplier does not exist.'
                })

            WaterBottle.objects.create(
                sku=sku,
                brand=brand,
                cost=cost,
                size=size,
                mouth_size=mouth_size,
                color=color,
                supplier=supplier,
                current_quantity=quantity
            )

            return redirect('view_bottles')

        return render(request, 'MyInventoryApp/add_bottle.html', {
            'supplier': Supplier.objects.all(),
            'user':current_user
        })
    else:
        return redirect('login')

    
def logout_view(request):
    global current_user
    current_user = None
    return redirect('login')

def change_password(request, pk):
    global current_user
    if current_user:
        if request.method == "POST":
            button = request.POST.get("button")

            if button == "confirm":
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                new_password2 = request.POST.get('new_password2')

                if not old_password or not new_password or not new_password2:
                    return render(request, 'MyInventoryApp/change_password.html', {'user': current_user, 'message': 'Please fill up ALL fields before submitting'})

                if new_password == new_password2:
                    if old_password == get_object_or_404(Account, pk=pk).getPassword():
                        Account.objects.filter(pk=pk).update(password=new_password)

                        request.session['message'] = 'Password changed successfully.'

                        return redirect('manage_account', pk=pk)

                    else:
                        message = "Input correct old password. Try again."
                        return render(request, 'MyInventoryApp/change_password.html', {'message': message, 'user': current_user})

                else:
                    message = "Unmatching passwords. Try again."
                    return render(request, 'MyInventoryApp/change_password.html', {'message': message, 'user': current_user})

            elif button == "cancel":
                return redirect('manage_account', pk=pk)
        
        else:
            return render(request, 'MyInventoryApp/change_password.html', {'user': current_user})
    else:
        return redirect('login')

    
def manage_account(request, pk):
    global current_user
    if current_user:
        if(request.method=="POST"):
            button = request.POST.get("button")

            if button == "delete_account":
                return redirect('delete_account', pk=pk)
        
        else:
            user = get_object_or_404(Account, pk=pk)
            message = request.session.pop('message', None)
            return render(request, 'MyInventoryApp/manage_account.html', {'user':user, 'message':message})
    else:
        return redirect('login')

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    request.session['message'] = 'Account deleted.'
    return redirect('login')

'''
Put this so that the log-in is required for every view.


    global current_user
    if current_user:
        <Your code>
    else:
        return redirect('login')

'''


