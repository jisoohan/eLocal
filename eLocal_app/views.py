from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ZipcodeForm

# Create your views here.
def homepage(request):
    if request.method == 'GET':
        form = ZipcodeForm()
    else:
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/products')
    return render(request, 'eLocal_app/homepage.html', {'form': form})

def productpage(request):
    return render(request, 'eLocal_app/productpage.html')
 

def shoppingPage(request):
    return render(request, 'eLocal_app/shoppingPage.html')


def storeSearchPage(request):
    return render(request, 'eLocal_app/storeSearchPage.html')


def addItemPage(request):
    return render(request, 'eLocal_app/addItemPage.html')