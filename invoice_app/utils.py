
from django.core.paginator import (
     Paginator, EmptyPage, PageNotAnInteger
     )

from .models import *

def pagination(request, model):
    # default_page 
        default_page = 1 
        page = request.GET.get('page', default_page)
        # paginate items
        items_per_page = 5
        paginator = Paginator(model, items_per_page)

        try:
            items_page = paginator.page(page)

        except PageNotAnInteger:
            items_page = paginator.page(default_page)

        except EmptyPage:
            items_page = paginator.page(paginator.num_pages) 

        return items_page

def get_total_paid(model, id):

    total = model.objects.all().filter(save_by=id, paid='True').count()
    return total

def get_total(model, id):

    obj = model.objects.filter(save_by=id).all()
    total = obj.count()
    return total 

def get_invoice(pk):
    """ get invoice fonction """
    obj = Invoice.objects.get(pk=pk)
    articles = obj.article_set.all()
    context = {
        'obj': obj,
        'articles': articles
    }
    return context

def get_customer(pk):
    """ get customer fonction """
    customer =Customer.objects.get(pk=pk)
    invoices = customer.invoice_set.all()
    total_invoices = invoices.count()
    total_paid = invoices.filter(paid='True').count()

    context = {
        'customer': customer,
        'invoices': invoices,
        'total_invoices': total_invoices,
        'total_paid': total_paid
    }
    return context

