import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pickle


model = tf.keras.models.load_model('model.keras')

with open('onehot_encoder_geo.pkl', 'rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

st.title("Customer Churn Prediction")


geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
cred_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_prod = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare input data
input_data = pd.DataFrame({
    'CreditScore': [cred_score],
    'Geography': [geography],
    'Gender': [gender],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_prod],  # Ensure the feature name matches the trained model
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# Encode categorical variables
geo_encoded = onehot_encoder_geo.transform(input_data[['Geography']]).toarray()
geo_feature_names = onehot_encoder_geo.get_feature_names_out(['Geography'])
geo_encoded_df = pd.DataFrame(geo_encoded, columns=geo_feature_names)

input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1).drop('Geography', axis=1)

gender_encoded = label_encoder_gender.transform(input_data['Gender'])
input_data['Gender'] = gender_encoded

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Predict
pred = model.predict(input_data_scaled)

# Display result
if pred[0][0] > 0.5:
    st.write('The customer is likely to churn')
else:
    st.write('The customer is not likely to churn')
