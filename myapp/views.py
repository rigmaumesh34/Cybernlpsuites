from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')



def home(request):
    return render(request,'home.html')


def signup(request):
    return render(request,'signup.html')


def password(request):
    return render(request,'form1.html')