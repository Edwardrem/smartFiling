from django.shortcuts import render, redirect
from .models import User, Importer, BillOfEntry, InternalDocument
from django.http import HttpResponse
from shipping_system import views

# User Views
def user_list(request):
    users = User.objects.all()

    query = request.GET.get('q')
    if query:
        users = users.filter(name__icontains=query)  # Filter users by name (case-insensitive)

    return render(request, 'users/user_list.html', {'users': users, 'query': query})

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

# Importer Views
def importer_list(request):
    importers = Importer.objects.all()

    query = request.GET.get('q')
    if query:
        importers = importers.filter(name__icontains=query)  # Filter importers by name (case-insensitive)

    return render(request, 'importers/importer_list.html', {'importers': importers, 'query': query})

def add_importer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_importer = Importer.objects.create(name=name)
        return redirect('importer_list')
    return render(request, 'importers/add_importer.html')

def edit_importer(request, importer_id):
    importer = Importer.objects.get(id=importer_id)
    if request.method == 'POST':
        importer.name = request.POST.get('name')
        importer.save()
        return redirect('importer_list')
    return render(request, 'importers/edit_importer.html', {'importer': importer})

def delete_importer(request, importer_id):
    importer = Importer.objects.get(id=importer_id)
    importer.delete()
    return redirect('importer_list')

# Bill of Entry Views
def bill_of_entry_list(request):
    bills_of_entry = BillOfEntry.objects.all()
    return render(request, 'bills/bill_of_entry_list.html', {'bills_of_entry': bills_of_entry})

def add_bill_of_entry(request):
    if request.method == 'POST':
        # Process form data and create a new bill of entry
        # Handle file uploads
        return redirect('bill_of_entry_list')
    return render(request, 'bills/add_bill_of_entry.html')

def edit_bill_of_entry(request, bill_of_entry_id):
    bill_of_entry = BillOfEntry.objects.get(id=bill_of_entry_id)
    if request.method == 'POST':
        # Process form data and update the bill of entry
        return redirect('bill_of_entry_list')
    return render(request, 'bills/edit_bill_of_entry.html', {'bill_of_entry': bill_of_entry})

def search_bill_of_entry(request):
    query = request.GET.get('q')
    bills_of_entry = BillOfEntry.objects.filter(description__icontains=query)
    return render(request, 'bills/bill_of_entry_list.html', {'bills_of_entry': bills_of_entry, 'query': query})

def preview_document(request, document_id):
    # Logic to preview the document
    return HttpResponse("Document Preview")

def download_document(request, document_id):
    # Logic to download the document
    return HttpResponse("Document Downloaded")

def delete_bill_of_entry(request, bill_of_entry_id):
    bill_of_entry = BillOfEntry.objects.get(id=bill_of_entry_id)
    bill_of_entry.delete()
    return redirect('bill_of_entry_list')