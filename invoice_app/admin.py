from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _


# Register your models here.

class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code')

class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'save_by', 'invoice_date_time', 'total', 'last_updated_date', 'paid', 'invoice_type')

class AdminEntrepreneur(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code', 'created_date', 'save_by', 'bank', 'bankaccount', 'swift', 'iban')

admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Entrepreneur, AdminEntrepreneur)
admin.site.register(Article)

admin.site.site_title = _("INVOICE SYSTEM MANAGER")
admin.site.site_header = _("INVOICE SYSTEM MANAGER")
admin.site.index_title = _("INVOICE SYSTEM MANAGER")

