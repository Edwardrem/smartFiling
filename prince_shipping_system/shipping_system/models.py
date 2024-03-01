from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('User', 'User'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Importer(models.Model):
    name = models.CharField(max_length=100)

class BillOfEntry(models.Model):
    importer = models.ForeignKey(Importer, on_delete=models.CASCADE)
    entry_number = models.CharField(max_length=50, unique=True)
    invoice_reference = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    attached_documents = models.FileField(upload_to='bills_of_entry/')

class InternalDocument(models.Model):
    company_name = models.CharField(max_length=100)
    document_name = models.CharField(max_length=100)
    description = models.TextField()
    attached_documents = models.FileField(upload_to='internal_documents/')