from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'eLocal_app/homepage.html')

def productpage(request):
    return render(request, 'eLocal_app/productpage.html')
