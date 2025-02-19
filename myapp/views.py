import os
from django.shortcuts import render
import pickle
from django.conf import settings
import joblib
from CyberNLPSuite import settings
from sklearn.feature_extraction.text import TfidfVectorizer as TfidfVectorize
from mlmodels.feature_extraction import *
import numpy as np


vectorizer_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'vectorizer.pkl')
model_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'password_model.pkl')
model_path2 = os.path.join(settings.BASE_DIR, 'mlmodels', 'random_forest_model.pkl')

vectorizer = joblib.load(vectorizer_path)
password_model = joblib.load(model_path)
url_model = joblib.load(model_path2)

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



def predict_url_type(url):
    """Extract features from the URL and predict its type."""
    try:
        features = extract_features(url)
        prediction = url_model.predict(features)# Extract first value
        return prediction
    except Exception as e:
        print(f"❌ URL Prediction Error: {e}")
        return -1  # Return -1 if prediction fails

def ure(request):
    if request.method == 'POST':
        urls = request.POST['url']
        print(f"🔎 URL Received: {urls}")

        prediction = predict_url_type(urls)
        print(f"🎯 URL Prediction: {prediction}")

        # ✅ Ensure valid prediction
        url_type = {0: 'benign', 1: 'defacement', 2: 'malware', 3: 'phishing'}
        url_label = url_type.get(int(prediction), 'Model Error')  # Handle unknown types
        print(f"🏷️ URL Label: {url_label}")
        return render(request, 'form1.html', {'url': urls, 'url_label': url_label})

    return render(request, 'form1.html')
# def predict_url_type(urls):
#     """Transform password and predict strength using trained model."""
#     f=extract_features(urls)

        
#     features = f.tolist() 
#     print(features)
#     prediction = url_model.predict(np.array(features)) 
#     print(prediction)
     
#     return prediction

# def ure(request):
#     if request.method == 'POST':
#         urls = request.POST['url']
#         print(urls)
 
#         types=predict_url_type(urls)
        
#         url_type= {0: 'benign', 1: 'defacement', 2: 'malware', 3: 'phishing'}
#         url_label = url_type.get(int(types), 'Model Not Loaded')
#         return render(request,'form1.html',{'url':urls,'url_label':url_label})
#     return render(request,'form1.html')

def XSS(request):
    if request.method == 'POST':
        code = request.POST['code']
        print(code)
        return render(request,'form1.html',{'code':code})
    return render(request,'form1.html')

