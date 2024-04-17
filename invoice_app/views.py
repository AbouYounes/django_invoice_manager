from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.

class HomeView(View):
    """ Main view """

    templates_name = 'index.html'
    invoices = Invoice.objects.select_related('customer', 'save_by').all()
    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwags):
        return render(request, self.templates_name, self.context)

    def post(self, request, *args, **kwagrs):
        # modify an invoice
        return render(request, self.templates_name, self.context)