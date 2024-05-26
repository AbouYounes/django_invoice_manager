from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),    
    path('customers/<int:pk>', views.CustomersView.as_view(), name="customers"),
    path('add-entrepreneur', views.AddEntrepreneurView.as_view(), name='add-entrepreneur'),
    path('add-customer', views.AddCustomerView.as_view(), name='add-customer'),
    path('add-invoice', views.AddInvoiceView.as_view(), name='add-invoice'),   
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('invoice-pdf/<int:pk>', views.get_invoice_pdf, name="invoice-pdf"),

]