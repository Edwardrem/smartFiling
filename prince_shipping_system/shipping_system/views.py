from django.shortcuts import render, redirect
from .models import User, Importer, BillOfEntry, InternalDocument
from shipping_system import views

# User Views
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        # Process form data and create a new user
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        new_user = User.objects.create(name=name, email=email, password=password, role=role)
        return redirect('user_list')
    return render(request, 'users/add_user.html')

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        # Process form data and update the user
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.role = request.POST.get('role')
        user.save()
        return redirect('user_list')
    return render(request, 'users/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users/user_list')