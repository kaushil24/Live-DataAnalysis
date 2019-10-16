import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
import os

st.title("Bank Marketing Analysis! ")



intro = "* The data is related with direct marketing campaigns of a Portuguese banking institution"
intro2 =    "* The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be (or not) subscribed."
st.markdown(intro)
st.markdown(intro2)

@st.cache
def get_data():
    return pd.read_csv(".\\Data\\bank-full.csv", sep=";")


st.markdown("## Exploratory data analyis")
st.write("* As listed above, the below mentioned dataset is regarding the marketing performed by some Portugese bank")
"* We need to predict wether the customer will **OPT IN** for a particular offer offered from the bank through telephonic marketing."



df = get_data()
x = st.slider("Number of rows to see", min_value = 5, max_value = 20)

st.dataframe(df.head(x), width=700, height = 600)

"#### Summary of various columns"
st.dataframe(df.describe())

st.write("It is clearly visible that the dataframe has no empty values")


# DISPLAYING PIE CHART #######################
st.markdown("### Distribution of those who opted in or out")

labels = ['Opted In', 'Opted Out']
values =list(df['y'].value_counts().values)

fig = go.Figure(data = go.Pie(labels=labels, values=values))
st.plotly_chart(fig)

st.markdown("""
Looking at the distribution of our output variable we can derive the following:\n
1. The number of people who opted in is considrabely greater than those who opted out. (88.3% vs 11.7%)\n
2. We need to take care so that the model does not become biased towards predcting positive outcome i.e. opt in
""")

# Distribution of various arrtibutes