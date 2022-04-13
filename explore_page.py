from json import load
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def shorten_category(category, threshold):
    cat_map = {}
    for i in range(len(category)):
        if category.values[i] >= threshold:
            cat_map[category.index[i]] = category.index[i]
        else:
            cat_map[category.index[i]] = 'Other'
    return cat_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedComp']]
    df = df.rename({'ConvertedComp': 'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop('Employment', axis=1)
    country_map = shorten_category(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df

df = load_data()

def show_explore_page():
    st.title('Explore Software Developer Salary')

    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')

    st.write('#### Number of data from different countries')
    st.pyplot(fig1)

    st.write('### Mean salary for each countries')

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write('### Mean salary for each level of experience')

    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)