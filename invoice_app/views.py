import datetime
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages
from django import forms


import pdfkit
from django.http import HttpResponse

from django.template.loader import get_template

from django.db import transaction
from .utils import get_customer, get_total, get_total_paid, pagination, get_invoice

from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import *
from django.contrib.auth.decorators import login_required


from django.utils.translation import gettext as _

@login_required
def dashboard(request):

    # POST method
    # Modifying an invoice   
    if request.POST.get('id_modified'):
            paid = request.POST.get('modified')
            try: 
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))
                if paid == 'True':
                    obj.paid = True 
                    obj.last_updated_date = request.POST.get('due-date')

                else:
                    obj.paid = False 
                    obj.last_updated_date = None
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

    id = request.user.id
    invoices = Invoice.objects.filter(user=id).all()
    customers = Customer.objects.filter(user=id).all()
    context = {
        'invoices': invoices,
        'customers' : customers,
    }

    items_inv = pagination(request, invoices)
    items_cust = pagination(request, customers)
    context['invoices'] = items_inv
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


# class HomeView(LoginRequiredMixin, View):

#     """ Main view """

#     templates_name = 'index.html'
#     invoices = Invoice.objects.filter(user=1).all()
#     customers = Customer.objects.filter(user=1).all()
#     article = Article.objects.select_related('save_by').all()
#     context = {
#         'invoices': invoices,
#         'customers' : customers,
#     }

#     def get(self, request, *args, **kwags):
#         items_inv = pagination_inv(request, self.invoices)
#         self.context['invoices'] = items_inv
#         items_cust = pagination_cus(request, self.customers)
#         self.context['customers'] = items_cust
#         # total invoice
#         total_invoices = get_total(Invoice)
#         self.context['total_invoices'] = total_invoices
#         # total customer
#         total_customers = get_total(Customer)
#         self.context['total_customers'] = total_customers 
#         # total paid
#         total_paid = get_total_paid(Invoice)
#         self.context['total_paid'] = total_paid
        
#         return render(request, self.templates_name, self.context)
    

#     def post(self, request, *args, **kwagrs):
#         # modify an invoice
#         if request.POST.get('id_modified'):
#             paid = request.POST.get('modified')
#             try: 
#                 obj = Invoice.objects.get(id=request.POST.get('id_modified'))
#                 if paid == 'True':
#                     obj.paid = True
#                 else:
#                     obj.paid = False 
#                 obj.save()
#                 messages.success(request,  _("Change made successfully."))
#             except Exception as e:   
#                 messages.error(request, _(f"Sorry, the following error has occured: {e}."))      

#         # deleting an invoice    
#         if request.POST.get('id_supprimer'):
#             try:
#                 obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
#                 obj.delete()
#                 messages.success(request, _("The deletion of invoice was successful."))   
#             except Exception as e:
#                 messages.error(request, _(f"Sorry, the following error has occured: {e}."))  

#         # deleting a customer    
#         if request.POST.get('id_customer_del'):
#             try:
#                 obj = Customer.objects.get(pk=request.POST.get('id_customer_del'))
#                 obj.delete()
#                 messages.success(request, _("The deletion of customer was successful."))   
#             except Exception as e:
#                 messages.error(request, _(f"Sorry, the following error has occured: {e}."))

#         items_inv = pagination_inv(request, self.invoices)
#         self.context['invoices'] = items_inv
#         items_cust = pagination_cus(request, self.customers)
#         self.context['customers'] = items_cust
#         Invoice.validate_constraints,
#         Customer.validate_constraints,
#         return render(request, self.templates_name, self.context)


@login_required
def entrepView(request):
    current_user= User.objects.get(id=request.user.id)
    profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=current_user)
    if request.method == 'POST' or profile_form.is_valid():
        profile_form.save()
        data = {
            'username': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'company_name': request.POST.get('company_name'),
            'created_date': request.POST.get('created_date'),
            'street': request.POST.get('street'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
            'country': request.POST.get('country'),
            'website': request.POST.get('website'),
            'bank_name': request.POST.get('bank_name'),
            'bank_account': request.POST.get('bank_account'),
            'swift': request.POST.get('swift'),
            'iban': request.POST.get('iban'),

        }
        try:
            updating =User.objects.filter(id=request.user.id).update(**data)
            if updating:
                messages.success(request, _("Entrepreneur updated successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))

        except Exception as e:    
            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    
    context = {
        'current_user': current_user,
        'profile_form': profile_form,
    }

    return render(request, 'add_entrepreneur.html', context) 

# class AddEntrepreneurView(LoginRequiredMixin, View):
#      """ add new entrepreneur """    
#      template_name = 'add_entrepreneur.html'
     
#      def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#      def post(self, request, *args, **kwargs):

#         data = {
#             'company': request.POST.get('company'),
#             'name': request.POST.get('name'),
#             'email': request.POST.get('email'),
#             'phone': request.POST.get('phone'),
#             'address': request.POST.get('address'),
#             'sex': request.POST.get('sex'),
#             'age': request.POST.get('age'),
#             'city': request.POST.get('city'),
#             'zip_code': request.POST.get('zip'),
#             'save_by': request.user

#         }

#         try:
#             created = Entrepreneur.objects.create(**data)
#             if created:
#                 messages.success(request, _("Entrepreneur registered successfully."))
#             else:
#                 messages.error(request, _("Sorry, please try again the sent data is corrupt."))
#         except Exception as e:    

#             messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

#         return render(request, self.template_name)   

@login_required
def addCustomer(request):
    if request.method == 'POST':
        data = {
            'user': request.user,
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
            'created_date': request.POST.get('created_date'),
        }
        print(data)
        try:
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, _("Customer registered successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))

        except Exception as e:    
            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    try:
        current_user= User.objects.filter(id=request.user.id).get()

    except Exception as e:    
        messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    return render(request, 'add_customer.html') 

# class AddCustomerView(LoginRequiredMixin, View):
#      """ add new customer """    
#      template_name = 'add_customer.html'
     
#      def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#      def post(self, request, *args, **kwargs):

#         data = {
#             'name': request.POST.get('name'),
#             'email': request.POST.get('email'),
#             'phone': request.POST.get('phone'),
#             'address': request.POST.get('address'),
#             'sex': request.POST.get('sex'),
#             'age': request.POST.get('age'),
#             'city': request.POST.get('city'),
#             'zip_code': request.POST.get('zip'),
#             'save_by': request.user

#         }

#         try:
#             created = Customer.objects.create(**data)
#             if created:
#                 messages.success(request, _("Customer registered successfully."))
#             else:
#                 messages.error(request, _("Sorry, please try again the sent data is corrupt."))
#         except Exception as e:    

#             messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

#         return render(request, self.template_name)   

@login_required
def addInvoice(request):

    current_user= User.objects.filter(id=request.user.id).get()
    customers = Customer.objects.filter(user=current_user).all()
    context = {
        'current_user': current_user,
        'customers': customers
    }

    if request.method == 'POST':
        last_order = Invoice.objects.all().filter(user=current_user).count()
        print('last_order: ', last_order)
        items = []

        try: 

            customer = request.POST.get('customer')
            new_order = last_order+1
            type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')
            date_a = request.POST.getlist('dt_a')
            qties = request.POST.getlist('qty')
            u_type = request.POST.getlist('ut_a')
            units = request.POST.getlist('unit')
            tax_a = request.POST.getlist('tax')
            total_a = request.POST.getlist('total-a')
            total = request.POST.get('total')
            comment1 = request.POST.get('comment1')
            comment2 = request.POST.get('comment2')
            invoice_object = {
                'user': request.user,
                'invoice_number': new_order,
                'customer_id': customer,
                'total': total,
                'invoice_type': type,
                'comment1': comment1,
                'comment2': comment2
            }

            print("Comment 1: ", comment1)
            print("Comment 2: ", comment2)

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
            
        
    return  render(request, 'add_invoice.html', context) 


# class AddInvoiceView(LoginRequiredMixin, View):
#     """ add a new invoice view """

#     template_name = 'add_invoice.html'
#     customers = Customer.objects.select_related('user').all()
#     entrepreneurs = Entrepreneur.objects.select_related('user').all()
#     context = {
#         'entrepreneurs': entrepreneurs,
#         'customers': customers
#     }

#     def get(self, request, *args, **kwargs):
#         return  render(request, self.template_name, self.context)
    
#     @transaction.atomic()
#     def post(self, request, *args, **kwargs):

#         items = []

#         try: 

#             entrepreneur = request.POST.get('entrepreneur')
#             customer = request.POST.get('customer')
#             type = request.POST.get('invoice_type')
#             articles = request.POST.getlist('article')
#             date_a = request.POST.getlist('dt_a')
#             qties = request.POST.getlist('qty')
#             u_type = request.POST.getlist('ut_a')
#             units = request.POST.getlist('unit')
#             tax_a = request.POST.getlist('tax')
#             total_a = request.POST.getlist('total-a')
#             total = request.POST.get('total')
#             comment = request.POST.get('commment')
#             invoice_object = {
#                 'entrepreneur_id': entrepreneur,
#                 'customer_id': customer,
#                 'total': total,
#                 'invoice_type': type,
#                 'comments': comment
#             }

#             invoice = Invoice.objects.create(**invoice_object)

#             for index, article in enumerate(articles):

#                 data = Article(
#                     invoice_id = invoice.id,
#                     name = article,
#                     article_date = date_a[index],
#                     quantity=qties[index],
#                     unit_type = u_type[index],
#                     unit_price = units[index],
#                     tva = tax_a[index],
#                     TTC_article = total_a[index]
#                 )

#                 items.append(data)

#             created = Article.objects.bulk_create(items)   

#             if created:
#                 messages.success(request, _("Data saved successfully.")) 
#             else:
#                 messages.error(request, _("Sorry, please try again the sent data is corrupt."))    

#         except Exception as e:
#             messages.error(request, _(f"Sorry the following error has occured: {e}."))  
        
#         return  render(request, self.template_name, self.context)
 

@login_required
def customerView(request, pk):
    context = get_customer(pk)
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
        }
        try: 
            updating = Customer.objects.filter(id=pk).update(**data)
            if updating:
                messages.success(request, _("Entrepreneur updated successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))

        except Exception as e:    
            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    try:
        context = get_customer(pk)

    except Exception as e:    
        messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

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
    
@login_required
def updateInvoiceView(request, pk):
    context = get_invoice(pk)
    customer = Customer.objects.filter(user=request.user.id)
    context['date'] = datetime.datetime.today()
    context['customer'] = customer
    print(context)

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
        }
        try: 
            updating = Customer.objects.filter(id=pk).update(**data)
            if updating:
                messages.success(request, _("Entrepreneur updated successfully."))
            else:
                messages.error(request, _("Sorry, please try again the sent data is corrupt."))

        except Exception as e:    
            messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    try:
        context = get_customer(pk)

    except Exception as e:    
        messages.error(request, _(f"Sorry our system is detecting the following issues: {e}"))

    return render(request, 'update_invoice.html', context)


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