import os
from django.shortcuts import render
import pickle
from django.conf import settings
import joblib
from CyberNLPSuite import settings
from sklearn.feature_extraction.text import TfidfVectorizer 
from mlmodels.feature_extraction import *
import numpy as np
from nltk.tokenize import word_tokenize
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import gensim
import pickle
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec










vectorizer_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'vectorizer.pkl')
model_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'password_model.pkl')
model_path2 = os.path.join(settings.BASE_DIR, 'mlmodels', 'random_forest_model.pkl')
word2vec_model_path = os.path.join(settings.BASE_DIR, 'mlmodels', 'word2vec_model.pkl')
model_path3 = os.path.join(settings.BASE_DIR, 'mlmodels', 'rf_classifier.pkl')


vectorizer = joblib.load(vectorizer_path)
password_model = joblib.load(model_path)
url_model = joblib.load(model_path2)
word2vecmodel = joblib.load(word2vec_model_path)
model = joblib.load(model_path3)
# with open(word2vec_model_path, 'rb') as file:
#     word2vector = pickle.load(file)
    
# with open(model_path3, 'rb') as file:
    
#     xss_model = pickle.load(file)




#word2vector = gensim.models.Word2Vec.load(word2vec_model_path)
# model = Word2Vec.load(word2vec_model_path)



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
        print(f"URL Prediction Error: {e}")
        return -1  # Return -1 if prediction fails

def ure(request):
    if request.method == 'POST':
        urls = request.POST['url']
        print(f" URL Received: {urls}")

        prediction = predict_url_type(urls)
        print(f"URL Prediction: {prediction}")

    
        url_type = {0: 'benign', 1: 'defacement', 2: 'malware', 3: 'phishing'}
        url_label = url_type.get(int(prediction), 'Model Error')  # Handle unknown types
        print(f"URL Label: {url_label}")
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
# def get_vector(text, model):
#     words = text.split()
#     if not any(word in model.wv for word in words):
#         return np.zeros(model.vector_size)
#     return np.mean((model.wv[word] for word in words if word in model.wv), axis=0)
def get_sentence_vectors(sentences, model):
    
    sentence_vectors = []
    
    for sentence in sentences:
        vector = []
        for word in word_tokenize(sentence.lower()):
            if word in model.wv:  # Check if word exists in Word2Vec vocabulary
                vector.append(model.wv[word])
            else:
                vector.append([0] * model.vector_size)  # Handle unknown words
        
        if vector:
            sentence_vectors.append(np.mean(np.array(vector), axis=0).tolist())  # Average vectors
        else:
            sentence_vectors.append([0] * model.vector_size)  # Zero vector for empty sentences
    
    return sentence_vectors


def XSS(request):
    if request.method == 'POST':
        code = request.POST['code']
        print(code)
        sentence_vector = get_sentence_vectors(code, word2vecmodel)
        print(sentence_vector)

        prediction = model.predict(sentence_vector)# Pedict using RF model
        print(prediction)
        prediction = "XSS Detected" if prediction[0]== 1 else "No XSS Found"

        return render(request, 'form1.html', {'code': code, 'prediction': prediction})

        
    return render(request,'form1.html')

