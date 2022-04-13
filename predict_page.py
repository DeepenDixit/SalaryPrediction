import streamlit as st
import numpy as np
import pickle

def load_model():
    with open('model_file.pkl','rb') as md:
        data = pickle.load(md)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title('Software Developer Salary Predictor')

    countries = ['Other', 'United States', 'India', 'United Kingdom', 'Germany', 'Canada', 'Brazil', 'France', 'Spain', 'Australia', 'Netherlands', 'Poland', 'Italy', 'Russian Federation', 'Sweden']
    education = ['Bachelor’s degree', 'Master’s degree', 'Less than a Bachelors', 'Post grad']

    country_sb = st.selectbox('Country',countries)
    education_sb = st.selectbox('Education Level',education)

    experience = st.slider('Years Of Experience', 0, 50, 3)

    get_button = st.button('Predict Salary')

    if get_button:
        X = np.array([[country_sb, education_sb, experience]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')
    else:
        pass