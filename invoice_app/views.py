import datetime
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

import pdfkit
from django.http import HttpResponse

from django.template.loader import get_template

from django.db import transaction
from .utils import get_customer, pagination, get_invoice

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import *

from django.utils.translation import gettext as _



class HomeView(LoginRequiredSuperuserMixim, View):
    """ Main view """

    templates_name = 'index.html'
    invoices = Invoice.objects.all()
    customers = Customer.objects.all()
    article = Article.objects.all()
    total_invoices = invoices.count()
    total_customers = customers.count()
    total_paid = invoices.filter(paid='True').count()
    context = {
        'invoices': invoices,
        'customers' : customers,
        'total_invoices' : total_invoices,
        'total_customers' : total_customers,
        'total_paid' : total_paid
    }
    Invoice.objects.alatest
    
    def get(self, request, *args, **kwags):
        items = pagination(request, self.invoices)
        self.context['invoices'] = items
        return render(request, self.templates_name, self.context)
    

    def post(self, request, *args, **kwagrs):

        # modify an invoice
        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')
            try: 
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))
                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False 
                obj.save()
                messages.success(request,  _("Change made successfully."))
            except Exception as e:   
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))      

        # deleting an invoice    
        if request.POST.get('id_supprimer'):
            try:
                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, _("The deletion was successful."))   
            except Exception as e:
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))  

        items = pagination(request, self.invoices)
        self.context['invoices'] = items
        Invoice.validate_constraints,
        return render(request, self.templates_name, self.context)

class AddEntrepreneurView(LoginRequiredSuperuserMixim, View):
     """ add new entrepreneur """    
     template_name = 'add_entrepreneur.html'
     
     def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

     def post(self, request, *args, **kwargs):

        data = {
            'company': request.POST.get('company'),
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user

        }

        try:
            created = Entrepreneur.objects.create(**data)
            if created:
                messages.success(request, _("Entrepreneur registered successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))
        except Exception as e:    

            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

        return render(request, self.template_name)   


class AddCustomerView(LoginRequiredSuperuserMixim, View):
     """ add new customer """    
     template_name = 'add_customer.html'
     
     def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

     def post(self, request, *args, **kwargs):

        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user

        }

        try:
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, _("Customer registered successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))
        except Exception as e:    

            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

        return render(request, self.template_name)   


class AddInvoiceView(LoginRequiredSuperuserMixim, View):
    """ add a new invoice view """

    template_name = 'add_invoice.html'
    customers = Customer.objects.select_related('save_by').all()
    entrepreneurs = Entrepreneur.objects.select_related('save_by').all()
    context = {
        'entrepreneurs': entrepreneurs,
        'customers': customers
    }

    def get(self, request, *args, **kwargs):
        return  render(request, self.template_name, self.context)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):

        items = []

        try: 

            entrepreneur = request.POST.get('entrepreneur')
            customer = request.POST.get('customer')
            type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')
            date_a = request.POST.getlist('dt_a')
            qties = request.POST.getlist('qty')
            u_type = request.POST.getlist('ut_a')
            units = request.POST.getlist('unit')
            tax_a = request.POST.getlist('tax')
            total_a = request.POST.getlist('total-a')
            total = request.POST.get('total')
            comment = request.POST.get('commment')
            invoice_object = {
                'entrepreneur_id': entrepreneur,
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comments': comment
            }

            invoice = Invoice.objects.create(**invoice_object)

            for index, article in enumerate(articles):

                data = Article(
                    invoice_id = invoice.id,
                    name = article,
                    article_date = date_a[index],
                    quantity=qties[index],
                    unit_type = u_type[index],
                    unit_price = units[index],
                    tva = tax_a[index],
                    TTC_article = total_a[index]
                )

                items.append(data)

            created = Article.objects.bulk_create(items)   

            if created:
                messages.success(request, _("Data saved successfully.")) 
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))    

        except Exception as e:
            messages.error(request, _(f"Sorry the following error has occured: {e}."))  
        
        return  render(request, self.template_name, self.context)
 

class CustomerView(LoginRequiredSuperuserMixim, View):
    """ Customer view """    
    
    template_name = 'customer.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_customer(pk)
        return render(request, self.template_name, context)
    
    
class InvoiceVisualizationView(LoginRequiredSuperuserMixim, View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_invoice(pk)
        return render(request, self.template_name, context)
    
   
@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')
    context = get_invoice(pk)
    context['date'] = datetime.datetime.today()

    path_wkthmltopdf = b'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    # get html file
    template = get_template('invoice-pdf.html')

    # render html with context variables
    html = template.render(context)

    # options of pdf format 
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
    }

    # generate pdf 
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachement: filename="sample.pdf"'

    return response

        
#       @superuser_required
 #       def get_invoice_pdf(request, *args, **kwargs):
  #          """ generate pdf file from html file """
#
 #           pk = kwargs.get('pk')
  #          context = get_invoice(pk)
   #         context['date'] = datetime.datetime.today()
#
 #           # get html file
  #          template = get_template('invoice-pdf.html')
#
 #           # render html with context variables
  #          html = template.render(context)
#
 #           # options of pdf format
  #          options = {
   #             'page-size': 'A4',
    #            'encoding': 'UTF-8',
     #           "enable-local-file-access": ""
      #      }
#
 #           # generate pdf
  #          pdf = pdfkit.from_string(html, False, options)
   #         #pdf = pdfkit.from_string(html, options=options, configuration=config)
    #        response = HttpResponse(pdf, content_type='application/pdf')
     #       response['Content-Disposition'] = "attachement"
#
 #           return response