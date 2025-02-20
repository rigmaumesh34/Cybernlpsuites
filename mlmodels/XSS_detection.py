# import numpy as np
# import gensim
# import pickle
# import nltk
# from nltk.tokenize import word_tokenize
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# import pandas as pd
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory

# model_path = os.path.join(BASE_DIR, "XSS_detction\\xssmodel.pkl")
# dataset_path = os.path.join(BASE_DIR, "XSS_dataset.csv")
# data = pd.read_csv(dataset_path, on_bad_lines='skip')


 
 
# with open(model_path, "rb") as file:
#     model = pickle.load(file)

# X = data.drop(columns=['Unnamed: 0','Label'])
 

# # Load and preprocess data (Assuming 'X' and 'data' are pre-loaded DataFrames)
# corpus_text = '\n'.join(X['Sentence'])
# datas = [[word.lower() for word in word_tokenize(sent)] for sent in nltk.sent_tokenize(corpus_text)]

# # Train Word2Vec model
# word2vec_model = gensim.models.Word2Vec(datas, min_count=1, vector_size=100, window=5, sg=0)

# # Convert sentences to vectors
# sentence_vectors = []
# for sentence in X['Sentence']:
#     vector = [word2vec_model.wv[word] if word in word2vec_model.wv else [0] * 100 for word in word_tokenize(sentence.lower())]
#     sentence_vectors.append(np.mean(np.array(vector), axis=0).tolist() if vector else [0] * 100)

# X_vectors = np.array(sentence_vectors)
# y_labels = data['Label'].values

# # Train-Test Split
# X_train, X_test, y_train, y_test = train_test_split(X_vectors, y_labels, test_size=0.2, random_state=42)

# # Train RandomForestClassifier
# rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# rf_classifier.fit(X_train, y_train)

# # Save the trained model
# with open("xssmodel.pkl", "wb") as file:
#     pickle.dump(rf_classifier, file)

# with open("word2vec.pkl", "wb") as file:
#     pickle.dump(word2vec_model, file)


