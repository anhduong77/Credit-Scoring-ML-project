import streamlit as st
import pandas as pd
import requests

st.title("Credit Scoring Prediction")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    row_idx = st.number_input("Select row index:", min_value=0, max_value=len(df)-1, step=1)

    if st.button("Predict selected row"):
        features = df.iloc[row_idx].to_dict()
        response = requests.post("http://127.0.0.1:8000/predict", json=features)

        if response.status_code == 200:
            st.write("Probability of default:", response.text)
        else:
            st.error(f"Error: {response.text}")

