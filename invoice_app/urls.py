from django.urls import path
from django.conf.urls.static import static

from django_invoice_manager import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [     
    #path('', views.dashboard, name='home'),    
    path('', views.dashboard, name='home'),    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),    

    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('register/', views.register, name='register'),


    path('customer/<int:pk>', views.customerView, name="customer"),
    path('add-entrepreneur', views.entrepView, name='add-entrepreneur'),
    path('add-customer', views.addCustomer, name='add-customer'),
    path('add-invoice', views.addInvoice, name='add-invoice'),   
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('update-invoice/<int:pk>', views.updateInvoiceView, name='update-invoice'),
    path('invoice-pdf/<int:pk>', views.get_invoice_pdf, name="invoice-pdf"),

]