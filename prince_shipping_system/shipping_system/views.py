from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Importer, BillOfEntry, InternalDocument
from django.contrib.auth.decorators import login_required
import mimetypes
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from shipping_system import views
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os





#Login Views
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Add error handling for invalid login
            return render(request, 'login.html', {'error': 'Invalid credentials. Please try again.'})
    return render(request, 'login.html')

# User Views
def user_list(request):
    users = User.objects.all()
    title='Users'

    query = request.GET.get('q')
    if query:
        users = users.filter(name__icontains=query)  # Filter users by name (case-insensitive)

    return render(request, 'users/user_list.html', {'users': users, 'query': query},)

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
    importers = Importer.objects.all()
    
    if request.method == 'POST':
        # Process form data and create a new bill of entry
        # Handle file uploads
        importer_name = request.POST.get('importer')
        entry_number = request.POST.get('entry_number')
        invoice_reference = request.POST.get('invoice_reference')
        description = request.POST.get('description')
        
        # Handle file upload
        attached_document = request.FILES.get('documents')
        
        # Create a new BillOfEntry object
        importer_instance = Importer.objects.get(id=importer_name)
        new_bill_of_entry = BillOfEntry.objects.create(
            importer=importer_instance,
            entry_number=entry_number,
            invoice_reference=invoice_reference,
            description=description,
            attached_documents=attached_document
        )
        
        # Save the new bill of entry
        new_bill_of_entry.save()
        return redirect('bill_of_entry_list')
    return render(request, 'bills/add_bill_of_entry.html', {'importers': importers})

def edit_bill_of_entry(request, bill_of_entry_id):
    importers = Importer.objects.all()
    bill_of_entry = BillOfEntry.objects.get(id=bill_of_entry_id)
    if request.method == 'POST':
        # Process form data and update the bill of entry
        importer_id = request.POST.get('importer')
        entry_number = request.POST.get('entry_number')
        invoice_reference = request.POST.get('invoice_reference')
        description = request.POST.get('description')
        
        # Handle file upload
        attached_document = request.FILES.get('documents')
        
        # Update the existing BillOfEntry object
        bill_of_entry.importer = Importer.objects.get(id=importer_id)
        bill_of_entry.entry_number = entry_number
        bill_of_entry.invoice_reference = invoice_reference
        bill_of_entry.description = description
        if attached_document:
            bill_of_entry.attached_document = attached_document
        
        # Save the updated bill of entry
        bill_of_entry.save()
        return redirect('bill_of_entry_list')
    return render(request, 'bills/edit_bill_of_entry.html', {'bill_of_entry': bill_of_entry, 'importers': importers})

def search_bill_of_entry(request):
    query = request.GET.get('q')
    bills_of_entry = BillOfEntry.objects.filter(description__icontains=query)
    return render(request, 'bills/bill_of_entry_list.html', {'bills_of_entry': bills_of_entry, 'query': query})

def preview_document(request, document_id):
    bill_of_entry = BillOfEntry.objects.get(id=document_id)
    file_path = bill_of_entry.attached_documents.name  # Get the file path of the attached document
    file_name = bill_of_entry.attached_documents.name.split('/')[-1]  # Extract the file name

    # Check if the file is a PDF
    if file_path.endswith('.pdf'):
        # Serve the PDF file for preview
        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
            return response
    else:
        return HttpResponse("Document Preview is not available for this file type.")

def download_document(request, document_id):
    # Retrieve the BillOfEntry object based on the document_id
    bill_of_entry = get_object_or_404(BillOfEntry, id=document_id)
    
    # Get the file path of the attached document
    file_path = bill_of_entry.attached_documents.path
    
    # Set the appropriate content type for the response
    content_type = mimetypes.guess_type(file_path)[0]
    
    # Create a FileResponse with the file
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    
    # Set the content-disposition header for the response to trigger a download
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    
    return response

def delete_bill_of_entry(request, bill_of_entry_id):
    bill_of_entry = BillOfEntry.objects.get(id=bill_of_entry_id)
    bill_of_entry.delete()
    return redirect('bill_of_entry_list')

# Internal Document Views
def internal_document_list(request):
    internal_documents = InternalDocument.objects.all()
    return render(request, 'docs/internal_document_list.html', {'internal_documents': internal_documents})

def add_internal_document(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        document_name = request.POST.get('document_name')
        description = request.POST.get('description')
        attached_document = request.FILES.get('documents')
        
        # Create a new InternalDocument object
        new_internal_document = InternalDocument.objects.create(
            company_name=company_name,
            document_name=document_name,
            description=description,
            attached_documents=attached_document
        )
        new_internal_document.save()
        
        return redirect('internal_document_list')
    
    return render(request, 'docs/add_internal_document.html')

def edit_internal_document(request, internal_document_id):
    internal_document = InternalDocument.objects.get(id=internal_document_id)
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        document_name = request.POST.get('document_name')
        description = request.POST.get('description')
        attached_document = request.FILES.get('documents')
        
        internal_document.company_name = company_name
        internal_document.document_name = document_name
        internal_document.description = description
        attached_documents=attached_document
        internal_document.save()
        
        return redirect('internal_document_list')
    
    return render(request, 'docs/edit_internal_document.html', {'internal_document': internal_document})
def search_internal_document(request):
    query = request.GET.get('q')
    internal_documents = InternalDocument.objects.filter(description__icontains=query)
    return render(request, 'docs/internal_document_list.html', {'internal_documents': internal_documents, 'query': query})

def preview_internal_document(request, document_id):
    internal_document = InternalDocument.objects.get(id=document_id)
    file_path = internal_document.attached_documents.name  # Get the file path of the attached document
    file_name = internal_document.attached_documents.name.split('/')[-1]  # Extract the file name
    
    # Check if the file is a PDF
    if file_path.endswith('.pdf'):
        # Serve the PDF file for preview
        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
            return response
    else:
        return HttpResponse("Document Preview is not available for this file type.")

def download_internal_document(request, document_id):
    internal_documents = get_object_or_404(InternalDocument, id=document_id)
    
    # Logic to download the internal document file
    file_path = internal_documents.attached_documents.path
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(internal_documents.attached_documents.name)
        return response

def delete_internal_document(request, internal_document_id):
    internal_document = InternalDocument.objects.get(id=internal_document_id)
    internal_document.delete()
    return redirect('internal_document_list')

#home
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def my_account(request):
    user = request.user  # Get the current logged-in user
    return render(request, 'user/my_account.html', {'user': user})

def edit_user_details(request):
    user = request.user  # Get the current logged-in user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('my_account')
    return render(request, 'user/edit_user_details.html', {'user': user})

def user_logout(request):
    logout(request)
    return redirect('login_page')