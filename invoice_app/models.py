from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Entrepreneur(models.Model):
    """
    Name: Entrepreneur model definition
    Description: 
    author: karim.khattou@univ-tiaret.dz
    """
    SEX_TYPES = (
        ('M', _('Male')),
        ('F', _('Feminine')),
    )
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    bank = models.CharField(max_length=64)
    bankaccount = models.CharField(max_length=64)
    swift = models.CharField(max_length=64)
    iban = models.CharField(max_length=64)


    class Meta: 
        verbose_name = "Entrepreneur"
        verbose_name_plural = "Entrepreneur"

    def __str__(self):
        return self.name
    


class Customer(models.Model):
    """
    Name: Customer model definition
    Description: 
    author: karim.khattou@univ-tiaret.dz
    """
    SEX_TYPES = (
        ('M', _('Male')),
        ('F', _('Feminine')),
    )
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta: 
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    """
    Name: Invoice model definition
    Description: 
    author: karim.khattou@univ-tiaret.dz
    """

    INVOICE_TYPE = (
        ('R', _('RECEIPT')),
        ('P', _('PROFORMA INVOICE')),
        ('I', _('INVOICE'))
    )

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid  = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.customer.name}_{self.invoice_date_time}"

    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.TTC_article for article in articles)
        return total
    
class Article(models.Model):
    """
    Name: Article model definiton
    Descripiton: 
    Author: karim.khattou@univ-tiaret.dz
    """

    UNIT_TYPE = (
            ('H', _('Hour')),
            ('M', _('Meter')),
        )
    
    TAX = (
        (0, _('0%')),
        (0.17, _('17%')),
        (0.19, _('19%')),
    )


    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    article_date = models.DateField(auto_now_add=False)
    quantity = models.IntegerField()
    unit_type = models.CharField(max_length=1, choices=UNIT_TYPE)
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    tva = models.DecimalField(max_digits=2, decimal_places=2, choices=TAX)
    TTC_article = models.DecimalField(max_digits=1000, decimal_places=2)
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        total = self.quantity  * self.unit_price 
        TTC_article = total  * (self.tva + 1)
        return round(TTC_article, 2) 

   