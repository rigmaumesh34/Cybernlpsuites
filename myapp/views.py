import os
from django.shortcuts import render
import pickle
from django.conf import settings
import joblib
from CyberNLPSuite import settings
from sklearn.feature_extraction.text import TfidfVectorizer as TfidfVectorize


vectorizer_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'vectorizer.pkl')
model_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'password_model.pkl')


vectorizer = joblib.load(vectorizer_path)
password_model = joblib.load(model_path)


# Create your views here.
def index(request):
    return render(request,'index.html')



def home(request):
    return render(request,'home.html')


def signup(request):
    return render(request,'signup.html')




def predict_password_strength(password):
    """Transform password and predict strength using trained model."""
    
    password_vector = vectorizer.transform([password])  
    strength = password_model.predict(password_vector)[0]  
    return strength
     

def password(request):
    if request.method == 'POST':
        user_password = request.POST['password']
        predicted_strength = predict_password_strength(user_password)

        
        strength_map = {0: 'Weak', 1: 'Medium', 2: 'Strong'}
        strength_label = strength_map.get(predicted_strength, 'Model Not Loaded')

        return render(request, 'form1.html', {'password': user_password, 'strength': strength_label})

    return render(request, 'form1.html')





def ure(request):
    if request.method == 'POST':
        urls = request.POST['url']
        print(urls)
        return render(request,'form1.html',{'url':urls})
    return render(request,'form1.html')

def XSS(request):
    if request.method == 'POST':
        code = request.POST['code']
        print(code)
        return render(request,'form1.html',{'code':code})
    return render(request,'form1.html')

