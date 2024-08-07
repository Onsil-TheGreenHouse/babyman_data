import streamlit as st
import configparser
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

properties = configparser.ConfigParser()
properties.read('data.ini')
data = properties['DATA']
keys = list(data.keys())

day = []
weight = []
milk = []

for item in keys:
    info = data[item].split(',')
    info2 = [int(i) for i in info]
    _date = date(info2[0], info2[1], info2[2])
    day.append(_date)
    weight.append(info2[3])
    milk.append(info2[4])

data_dict = {
    'day': day,
    'weight': weight,
    'milk': milk
}
df = pd.DataFrame(data=data_dict)

today = day[-1]
birthday = date(2024, 5, 17)
expected_day = date(2024, 7, 19)

st.header(f'애기맨 몸무게/우유 차트({today})')

# baby_select_sidebar = st.sidebar.selectbox(
#     'Select Baby',
#     ('박승우',)
# )

container = st.container(border=True)
birth_age_day = (today - birthday).days
birth_age_week = int(birth_age_day/7)
correction_age_day = (today - expected_day).days
correction_age_week = int(correction_age_day/7)

container.write(f'출생나이:   {birth_age_day}일({birth_age_week}주)')
container.write(f'교정나이:   {correction_age_day}일({correction_age_week}주)')

col1, col2 = st.columns(2)
col1.metric(label='오늘의 몸무게(g)', value=str(weight[-1])+'g', delta=str(weight[-1]-weight[-2])+'g')
col2.metric(label='오늘의 수유량(cc)', value=str(milk[-1])+'cc', delta=str(milk[-1]-milk[-2])+'cc')

# fig = px.line(df, x='day', y='weight', markers=True)
# fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=df['day'], y=df['weight'], mode='lines+markers', name='weight', marker_color='red'))
fig.add_trace(go.Scatter(x=df['day'], y=df['milk'], mode='lines+markers', name='milk'), secondary_y=True)
fig.update_layout(
    yaxis=dict(
        title=dict(text='weight(g)'),
        side='left',
        range=[1400, 4000]
    ),
    yaxis2=dict(
        title=dict(text='milk(cc)'),
        side='right',
        range=[0, 200]
    )
)

# col3, col4 = st.columns([55, 45])
# with col3:
st.plotly_chart(fig, use_container_width=True)
# with col4:
st.dataframe(df, use_container_width=True)
    # st.dataframe(df.set_index(df.columns[0]))
    # st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)