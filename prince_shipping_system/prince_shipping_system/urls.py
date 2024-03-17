"""
URL configuration for prince_shipping_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from shipping_system import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('importers/', views.importer_list, name='importer_list'),
    path('importers/add/', views.add_importer, name='add_importer'),
    path('importers/<int:importer_id>/edit/', views.edit_importer, name='edit_importer'),
    path('importers/<int:importer_id>/delete/', views.delete_importer, name='delete_importer'),
    path('bills_of_entry/', views.bill_of_entry_list, name='bill_of_entry_list'),
    path('bills_of_entry/add/', views.add_bill_of_entry, name='add_bill_of_entry'),
    path('bills_of_entry/<int:bill_of_entry_id>/edit/', views.edit_bill_of_entry, name='edit_bill_of_entry'),
    path('bills_of_entry/search/', views.search_bill_of_entry, name='search_bill_of_entry'),
    path('bills_of_entry/<int:document_id>/preview/', views.preview_document, name='preview_document'),
    path('bills_of_entry/<int:document_id>/download/', views.download_document, name='download_document'),
    path('bills_of_entry/<int:bill_of_entry_id>/delete/', views.delete_bill_of_entry, name='delete_bill_of_entry'),
    path('internal_documents/', views.internal_document_list, name='internal_document_list'),
    path('internal_documents/add/', views.add_internal_document, name='add_internal_document'),
    path('internal_documents/<int:internal_document_id>/edit/', views.edit_internal_document, name='edit_internal_document'),
    path('internal_documents/search/', views.search_internal_document, name='search_internal_document'),
    path('internal_documents/<int:document_id>/preview/', views.preview_internal_document, name='preview_internal_document'),
    path('internal_documents/<int:document_id>/download/', views.download_internal_document, name='download_internal_document'),
    path('internal_documents/<int:internal_document_id>/delete/', views.delete_internal_document, name='delete_internal_document'),
    path('my-account/', views.my_account, name='my_account'),
    path('my-account/edit/', views.edit_user_details, name='edit_user_details'),
    path('logout/', views.user_logout, name='logout'),
]
