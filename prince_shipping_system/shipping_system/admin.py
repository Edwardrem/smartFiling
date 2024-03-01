from django.contrib import admin
from .models import User, Importer, BillOfEntry, InternalDocument

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role')

@admin.register(Importer)
class ImporterAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BillOfEntry)
class BillOfEntryAdmin(admin.ModelAdmin):
    list_display = ('importer', 'entry_number', 'invoice_reference', 'description')

@admin.register(InternalDocument)
class InternalDocumentAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'document_name', 'description')