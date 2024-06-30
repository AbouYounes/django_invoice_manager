import datetime
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

import pdfkit
from django.http import HttpResponse

from django.template.loader import get_template

from django.db import transaction
from .utils import get_customer, get_total, get_total_paid, pagination_cus, pagination_inv, get_invoice

from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import *
from django.contrib.auth.decorators import login_required


from django.utils.translation import gettext as _

@login_required
def dashboard(request):
    id = 0
    if request.user.is_authenticated:
        id = request.user.id

    invoices = Invoice.objects.filter(save_by=id).all()
    customers = Customer.objects.filter(save_by=id).all()
    article = Article.objects.select_related('save_by').all()
    context = {
        'invoices': invoices,
        'customers' : customers,
    }

    items_inv = pagination_inv(request, invoices)
    context['invoices'] = items_inv
    items_cust = pagination_cus(request, customers)
    context['customers'] = items_cust
    # total invoice
    total_invoices = get_total(Invoice, id)
    context['total_invoices'] = total_invoices
    # total customer
    total_customers = get_total(Customer, id)
    context['total_customers'] = total_customers 
    # total paid
    total_paid = get_total_paid(Invoice, id)
    context['total_paid'] = total_paid

    items_inv = pagination_inv(request, invoices)
    context['invoices'] = items_inv
    items_cust = pagination_cus(request, customers)
    context['customers'] = items_cust
    Invoice.validate_constraints,
    Customer.validate_constraints,

    return render(request, 'dashboard.html', context)
    

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object
            new_user = user_form.save(commit=False)
            
            #set the choosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            #save the new object
            new_user.save()
            return render(request, 'register_confirm.html', {'new_user': new_user})
            
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


class HomeView(LoginRequiredMixin, View):

    """ Main view """

    templates_name = 'index.html'
    invoices = Invoice.objects.filter(save_by=1).all()
    customers = Customer.objects.filter(save_by=1).all()
    article = Article.objects.select_related('save_by').all()
    context = {
        'invoices': invoices,
        'customers' : customers,
    }

    def get(self, request, *args, **kwags):
        items_inv = pagination_inv(request, self.invoices)
        self.context['invoices'] = items_inv
        items_cust = pagination_cus(request, self.customers)
        self.context['customers'] = items_cust
        # total invoice
        total_invoices = get_total(Invoice)
        self.context['total_invoices'] = total_invoices
        # total customer
        total_customers = get_total(Customer)
        self.context['total_customers'] = total_customers 
        # total paid
        total_paid = get_total_paid(Invoice)
        self.context['total_paid'] = total_paid

        id = 0
        if request.user.is_authenticated:
            id = request.user.id

        print('id= ',id)

        
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
                messages.success(request, _("The deletion of invoice was successful."))   
            except Exception as e:
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))  

        # deleting a customer    
        if request.POST.get('id_customer_del'):
            try:
                obj = Customer.objects.get(pk=request.POST.get('id_customer_del'))
                obj.delete()
                messages.success(request, _("The deletion of customer was successful."))   
            except Exception as e:
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))

        items_inv = pagination_inv(request, self.invoices)
        self.context['invoices'] = items_inv
        items_cust = pagination_cus(request, self.customers)
        self.context['customers'] = items_cust
        Invoice.validate_constraints,
        Customer.validate_constraints,
        return render(request, self.templates_name, self.context)


@login_required
def entrepView(request):
    if request.user.is_authenticated:
        id = request.user.id 
    try: 
        if Firma.objects.filter(id=id).exists():
            firma = Firma.objects.filter(id=id).get()
        else:
            data = {
                'name': request.user.first_name,
                'email': request.user.email,
            }
            try:
                created = Firma.objects.create(**data)
                if created:
                    messages.success(request, _("Entrepreneur updated successfully."))
                else:
                    messages.error(request, _("Sorry, please try again the sent data is corrupt."))
            except Exception as e:    

                messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    except Exception as e:    
        messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))
        
    if request.method == 'POST':
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
            'logo': request.POST.get('logo'),

        }
        try:
            created = Firma.objects.update(**data)
            if created:
                messages.success(request, _("Entrepreneur updated successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))
        except Exception as e:    

            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    firma = Firma.objects.filter(id=id).get()
    context = {'firma': firma}
    return render(request, 'add_entrepreneur.html', context) 

class AddEntrepreneurView(LoginRequiredMixin, View):
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


class AddCustomerView(LoginRequiredMixin, View):
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


class AddInvoiceView(LoginRequiredMixin, View):
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
 

@login_required
def customerView(request, pk):
    context = get_customer(pk)
    return render(request, 'customer.html', context)


class CustomerView(LoginRequiredMixin, View):
    """ Customer view """    
    
    template_name = 'customer.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_customer(pk)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwagrs):
        # modify a customer
        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')
            try: 
                obj = Customer.objects.get(id=request.POST.get('id_modified'))
                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False 
                obj.save()
                messages.success(request,  _("Change made successfully."))
            except Exception as e:   
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))      

        # deleting a invoice    
        if request.POST.get('id_supprimer'):
            try:
                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, _("The deletion of invoice was successful."))   
            except Exception as e:
                messages.error(request, _(f"Sorry, the following error has occured: {e}."))  

        items_inv = pagination_inv(request, self.invoices)
        self.context['invoices'] = items_inv
        items_cust = pagination_cus(request, self.customers)
        self.context['customers'] = items_cust
        Invoice.validate_constraints,
        Customer.validate_constraints,
        return render(request, self.templates_name, self.context)
    
    
class InvoiceVisualizationView(LoginRequiredMixin, View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_invoice(pk)
        return render(request, self.template_name, context)
    

@login_required
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