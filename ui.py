import pickle
import streamlit as st
import pandas as pd
import base64

credit_model = pickle.load(open('credit_model.sav', 'rb'))

form = st.form("credit_form", clear_on_submit=True)
form.title('Form Credit Card Approval', 'rb')

uploaded_file = form.file_uploader("Upload CSV File")

# Tombol untuk memproses file CSV
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    credit_predict = credit_model.predict(df)
    
    # Menampilkan hasil prediksi
    st.write("Data CSV:")
    st.write(df)
    
    st.write("Predictions:")
    st.write(credit_predict)

    # Tombol untuk mengunduh hasil prediksi
    csv = df.copy()
    csv['Prediction'] = credit_predict
    csv_file = csv.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="predictions.csv">Download Predictions</a>'
    st.markdown(href, unsafe_allow_html=True)

## Menampilkan annual income
AMT_INCOME_TOTAL = form.number_input('Input Annual Income', min_value=0, value=0)

## Menampilkan education type
NAME_EDUCATION_TYPE = form.selectbox('Education Type', ('Choose one', 'Academic degree', 'Higher education', 
                                                        'Incomplete higher', 'Lower secondary', 
                                                        'Secondary / secondary special'))

if NAME_EDUCATION_TYPE == 'Academic degree':
    NAME_EDUCATION_TYPE = 0
elif NAME_EDUCATION_TYPE == 'Higher education':
    NAME_EDUCATION_TYPE = 1
elif NAME_EDUCATION_TYPE == 'Incomplete higher':
    NAME_EDUCATION_TYPE = 2
elif NAME_EDUCATION_TYPE == 'Lower secondary':
    NAME_EDUCATION_TYPE = 3
elif NAME_EDUCATION_TYPE == 'Secondary / secondary special':
    NAME_EDUCATION_TYPE = 4

# Menampilkan family status
NAME_FAMILY_STATUS = form.selectbox('Family Status', ('Choose one', 'Civil marriage', 'Married', 
                                                      'Separated', 'Single / not married', 'Widow'))
if NAME_FAMILY_STATUS == 'Civil marriage':
    NAME_FAMILY_STATUS = 0
elif NAME_FAMILY_STATUS == 'Married':
    NAME_FAMILY_STATUS = 1
elif NAME_FAMILY_STATUS == 'Separated':
    NAME_FAMILY_STATUS = 2
elif NAME_FAMILY_STATUS == 'Single / not married':
    NAME_FAMILY_STATUS = 3
elif NAME_FAMILY_STATUS == 'Widow':
    NAME_FAMILY_STATUS = 4

## Menampilkan occupation
OCCUPATION_TYPE = form.selectbox('Occupation Type', ('Choose one', 'Accountants', 'Cleaning staff', 'Cooking staff', 
                                                     'Core staff', 'Drivers', 'High skill tech staff', 'HR staff', 
                                                     'IT staff', 'Laborers', 'Low-skill Laborers', 'Managers', 
                                                     'Medicine staff', 'Not working', 'Others', 
                                                     'Private service staff', 'Realty agents', 'Sales staff', 
                                                     'Secretaries', 'Security staff', 'Waiters/barmen staff'))

if OCCUPATION_TYPE == 'Accountants':
    OCCUPATION_TYPE = 0
elif OCCUPATION_TYPE == 'Cleaning staff':
    OCCUPATION_TYPE = 1
elif OCCUPATION_TYPE == 'Cooking staff':
    OCCUPATION_TYPE = 2
elif OCCUPATION_TYPE == 'Core staff':
    OCCUPATION_TYPE = 3
elif OCCUPATION_TYPE == 'Drivers':
    OCCUPATION_TYPE = 4
elif OCCUPATION_TYPE == 'High skill tech staff':
    OCCUPATION_TYPE = 5
elif OCCUPATION_TYPE == 'HR staff':
    OCCUPATION_TYPE = 6
elif OCCUPATION_TYPE == 'IT staff':
    OCCUPATION_TYPE = 7
elif OCCUPATION_TYPE == 'Laborers':
    OCCUPATION_TYPE = 8
elif OCCUPATION_TYPE == 'Low-skill Laborers':
    OCCUPATION_TYPE = 9
elif OCCUPATION_TYPE == 'Managers':
    OCCUPATION_TYPE = 10
elif OCCUPATION_TYPE == 'Medicine staff':
    OCCUPATION_TYPE = 11
elif OCCUPATION_TYPE == 'Not working':
    OCCUPATION_TYPE = 12
elif OCCUPATION_TYPE == 'Others':
    OCCUPATION_TYPE = 13
elif OCCUPATION_TYPE == 'Private service staff':
    OCCUPATION_TYPE = 14
elif OCCUPATION_TYPE == 'Realty agents':
    OCCUPATION_TYPE = 15
elif OCCUPATION_TYPE == 'Sales staff':
    OCCUPATION_TYPE = 16
elif OCCUPATION_TYPE == 'Secretaries':
    OCCUPATION_TYPE = 17
elif OCCUPATION_TYPE == 'Security staff':
    OCCUPATION_TYPE = 18
elif OCCUPATION_TYPE == 'Waiters/barmen staff':
    OCCUPATION_TYPE = 19

## Menampilkan age
AGE  = form.number_input('Input Age', min_value=0, max_value=100, value=0, step=1)

## Menampilkan working year
WORKING_YEAR  = form.number_input('Input Working Year', min_value=0, max_value=100, value=0, step=1)

col1, col2 = form.columns([4,1])
## code untuk prediksi
credit_result = ''

## tombol predict
if col1.form_submit_button('Prediksi Credit Card Approval'):
    if NAME_EDUCATION_TYPE == 'Choose one' or NAME_FAMILY_STATUS == 'Choose one' or OCCUPATION_TYPE == 'Choose one':
        form.error('All column must be filled')
    elif AGE < 17:
        form.error('Minimal age must be 17')
    else:
        credit_predict = credit_model.predict([[AMT_INCOME_TOTAL, NAME_EDUCATION_TYPE, NAME_FAMILY_STATUS, 
                                                OCCUPATION_TYPE, AGE, WORKING_YEAR]])

        if (credit_predict[0] == 1):
            credit_result = 'Customer Low Risk'
            form.success(credit_result)
        else:
            credit_result = 'Customer High Risk'
            form.error(credit_result)

if col2.form_submit_button(':wastebasket: Clear Input'):
    AMT_INCOME_TOTAL = 0
    NAME_EDUCATION_TYPE = 'Choose one'
    NAME_FAMILY_STATUS = 'Choose one'
    OCCUPATION_TYPE = 'Choose one'
    AGE = 0
    WORKING_YEAR = 0
