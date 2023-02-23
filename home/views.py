from django.shortcuts import render
from products.models import Product
# Create your views here.

def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'home.html' , context)