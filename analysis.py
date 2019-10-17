import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
import os
from PIL import Image
import plotly.figure_factory as ff
import seaborn as sns 


st.title("Bank Marketing Analysis! ")



intro = "* The data is related with direct marketing campaigns of a Portuguese banking institution"
intro2 =    "* The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be (or not) subscribed."
st.markdown(intro)
st.markdown(intro2)

@st.cache
def get_data():

    return pd.read_csv(os.path.join("Data", "Bank-full.csv"), sep=";")


st.markdown("## Exploratory data analyis")
st.write("* As listed above, the below mentioned dataset is regarding the marketing performed by some Portugese bank")
"* We need to predict wether the customer will **OPT IN** for a particular offer offered from the bank through telephonic marketing."



df = get_data()
x = st.slider("Number of rows to see", min_value = 5, max_value = 20)

st.dataframe(df.head(x), width=700, height = 600)

"### Summary of various columns"
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

# Showig corelation of each artibute #########
'''
### Corelation of each attribute among each other 
'''
try:
    image = Image.open('https://github.com/JoyMehta98/Bank_Merket_Analysis/blob/master/corelation.png')
    st.image(image, caption='Corelation Image', use_column_width=True)
except:
    pass
'''
### The following inference can be deduced:
* Most of the columns are distinct and not corelates
* This means, we do not need to perform any feature engineering and the raw columns can directly be used to perform analysis.
'''
# Distribution of various arrtibutes

"""
#### Select occcupation profile to view gausian distribution:
"""
try:
    profiles = st.multiselect("Choose occupation profile", list(df['job'].value_counts().index),['management'])   #, ["management", 'unknown'])

    hist_data = []
    for col in profiles:
        data = df.loc[df['job']==col, 'balance'][0:300]
        hist_data.append(list(data.values))


    fig = ff.create_distplot(hist_data, profiles, bin_size=[100 for _ in range(len(profiles))])
    st.plotly_chart(fig)
except Exception as e:
    e

# # # Plot!
# st.plotly_chart(fig)

# profiles = ['admin.', 'unknown']
# for vals in profiles:
#     # st.bar_chart(df.loc[df['job']==vals, 'balance'])
#     sns.distplot(df.loc[df['job']==vals, ['balance']], bins = 10)#, legend_out=True)
#     st.pyplot()    
# # fig.legend(labels=profiles)

# for vals in profiles:
#     st.dataframe(df.loc[df['job']==vals, 'balance'])

"""
#### Inference from the distribution of balance according to job profile:
* Housemaids jobs have highest standard deviation with respect to balance
* Retired prople have highest balance
* Student have the lowest balance and also have least standard deviation
* The balance of all the profiles is highly negatively skewed, meaning there are more number of people earning lesser balance in their respecive job profile.
"""

'''
### Understanding the maritial distribution and their balance
'''

vals = df['marital'].value_counts().tolist()
labels = ['married', 'divorced', 'single']

data = [go.Bar(
            x=labels,
            y=vals,
    marker=dict(
    color="#FE9A2E")
    )]

layout = go.Layout(
    title="Count by Marital Status",
)

fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

'''
#### Balance distribution according to marrital status:
'''
x = list((df['balance'].loc[df['marital']=='single']).values)
y = list((df['balance'].loc[df['marital']=='married']).values)
z = list((df['balance'].loc[df['marital']=='divorced']).values)
hist_data = [x[:200], y[:200], z[:200]]
status = ['single', 'married', 'divorced']
fig = ff.create_distplot(hist_data, status, bin_size=[100 for _ in range(len(status))])
st.plotly_chart(fig)

'''
#### Inferences:
* Singles have average minimum balance **HOWEVER** single has the maximum income.
* Married have on average maximum income.
'''


def balance_dis():
    # Create a Balance Category
    df["balance_status"] = np.nan
    lst = [df]

    for col in lst:
        col.loc[col["balance"] < 0, "balance_status"] = "negative"
        col.loc[(col["balance"] >= 0) & (col["balance"] <= 30000), "balance_status"] = "low"
        col.loc[(col["balance"] > 30000) & (col["balance"] <= 40000), "balance_status"] = "middle"
        col.loc[col["balance"] > 40000, "balance_status"] = "high"
        
    # balance by balance_status
    negative = df["balance"].loc[df["balance_status"] == "negative"].values.tolist()
    low = df["balance"].loc[df["balance_status"] == "low"].values.tolist()
    middle = df["balance"].loc[df["balance_status"] == "middle"].values.tolist()
    high = df["balance"].loc[df["balance_status"] == "high"].values.tolist()


    # Get the average by occupation in each balance category
    job_balance = df.groupby(['job', 'balance_status'])['balance'].mean()


    trace1 = go.Barpolar(
        r=[-199.0, -392.0, -209.0, -247.0, -233.0, -270.0, -271.0, 0, -276.0, -134.5],
        text=["blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed",
            "services", "student", "technician", "unemployed"],
        name='Negative Balance',
        marker=dict(
            color='rgb(246, 46, 46)'
        )
    )
    trace2 = go.Barpolar(
        r=[319.5, 283.0, 212.0, 313.0, 409.0, 274.5, 308.5, 253.0, 316.0, 330.0],
        text=["blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed",
            "services", "student", "technician", "unemployed"],
        name='Low Balance',
        marker=dict(
            color='rgb(246, 97, 46)'
        )
    )
    trace3 = go.Barpolar(
        r=[2128.5, 2686.0, 2290.0, 2366.0, 2579.0, 2293.5, 2005.5, 2488.0, 2362.0, 1976.0],
        text=["blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed",
            "services", "student", "technician", "unemployed"],
        name='Middle Balance',
        marker=dict(
            color='rgb(246, 179, 46)'
        )
    )
    trace4 = go.Barpolar(
        r=[14247.5, 20138.5, 12278.5, 12956.0, 20723.0, 12159.0, 12223.0, 13107.0, 12063.0, 15107.5],
        text=["blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed",
            "services", "student", "technician", "unemployed"],
        name='High Balance',
        marker=dict(
            color='rgb(46, 246, 78)'
        )
    )
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title='Mean Balance in Account<br> <i> by Job Occupation</i>',
        font=dict(
            size=12
        ),
        legend=dict(
            font=dict(
                size=16
            )
        ),
        radialaxis=dict(
            ticksuffix='%'
        ),
        orientation=270
    )
    return go.Figure(data=data, layout=layout)

st.plotly_chart(balance_dis())

