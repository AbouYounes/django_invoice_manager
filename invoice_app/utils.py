
from django.core.paginator import (
     Paginator, EmptyPage, PageNotAnInteger
     )

from .models import *

def pagination_inv(request, invoices):
    # default_page 
        default_page = 1 
        page = request.GET.get('page', default_page)
        # paginate items
        items_per_page = 3
        paginator = Paginator(invoices, items_per_page)

        try:
            items_page = paginator.page(page)

        except PageNotAnInteger:
            items_page = paginator.page(default_page)

        except EmptyPage:
            items_page = paginator.page(paginator.num_pages) 

        return items_page

def get_total_paid(model):

    total = model.objects.all().filter(paid='True').count()
    return total

def get_total(model):

    obj = model.objects.all()
    total = obj.count()
    return total 


def pagination_cus(request, customers):
    # default_page 
        default_page = 1 
        page = request.GET.get('page', default_page)
        # paginate items
        items_per_page = 3
        paginator = Paginator(customers, items_per_page)

        try:
            items_page = paginator.page(page)

        except PageNotAnInteger:
            items_page = paginator.page(default_page)

        except EmptyPage:
            items_page = paginator.page(paginator.num_pages) 

        return items_page 


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

    context = {
        'customer': customer,
        'invoices': invoices,
        'total_invoices': total_invoices
    }
    return context

