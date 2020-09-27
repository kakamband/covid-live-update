import streamlit as st
import pandas as pd
import numpy as np
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize
from streamlit.ScriptRunner import StopException, RerunException

fig = go.Figure()
hide_streamlit_style = """
        <title> Half Explot </title>
        <style>
        footer {visibility: hidden;}
        .sidebar .sidebar-content {background-image: linear-gradient(180deg,#5cbede,#e0debf00);}
        .st-b9 {background-color: rgb(47 38 47 / 76%);}
        .st-b4 {color: rgb(111 235 255);}
        .btn-outline-secondary {
        border-color: #09ab3b85;
        color: #f9f9f9;
        }
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("""
# مجموعه داده زنده کوید ۱۹ 🚨
[وب سرویس زنده کرونا ویروس کوید ۱۹](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest#81447902-b68a-4e79-9df9-1b371905e9fa)برای دریافت داده ها در این برنامه استفاده می شود.
""")

st.write('''
ویروس کرونا ویروس COVID-19 بحران تعیین کننده سلامت جهانی در زمان ما و بزرگترین چالشی است که از زمان جنگ جهانی دوم با آن روبرو بوده ایم.
از زمان ظهور در آسیا در اواخر سال گذشته ، ویروس به همه قاره ها به جز قطب جنوب گسترش یافته است.

اما همه گیری بسیار فراتر از بحران سلامت است ، همچنین یک بحران اقتصادی-اجتماعی بی سابقه است.

با تأکید بر هر یک از کشورهایی که لمس می کند ، این امکان را دارد که اجتماعی ویرانگر ایجاد کند ،
اثرات اقتصادی و سیاسی که جای زخمهای عمیق و طولانی مدت ایجاد خواهد کرد.''')

# st.markdown('<iframe src="https://datawrapper.dwcdn.net/WIdnc/5/" style="height:400px;width:800px;" title="Iframe Example"></iframe>', unsafe_allow_html=True)
st.markdown('<iframe src="https://datawrapper.dwcdn.net/JjgUp/2/" style="height:450px;width:700px;" title="Iframe Example"></iframe>', unsafe_allow_html=True)

url = 'https://api.covid19api.com/countries'
r = requests.get(url)
df0 = pd.json_normalize(r.json())

top_row = pd.DataFrame({'Country':['Select a Country'],'Slug':['Empty'],'ISO2':['E']})
# Concat with old DataFrame and reset the Index.
df0 = pd.concat([top_row, df0]).reset_index(drop = True)

st.sidebar.header('جستجوی خود را فیلتر کنید')
graph_type = st.sidebar.selectbox('نوع کیس آماری خود را از بین تایید شده ، فوت شدگان ، بهبود یافتگان انتخاب کنید',('confirmed','deaths','recovered'))
st.sidebar.subheader('جستجو بر اساس کشور 📌')
country = st.sidebar.selectbox('نام کشور',df0.Country)
country1 = st.sidebar.selectbox('مقایسه با کشور دیگر',df0.Country)
if st.sidebar.button('تازه کردن داده ها'):
  raise RerunException(st.ScriptRequestQueue.RerunData(None))

if country != 'یک کشور را انتخاب کنید':
    slug = df0.Slug[df0['Country']==country].to_string(index=False)[1:]
    url = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/'+graph_type
    r = requests.get(url)
    st.write("""# Total """+graph_type+""" cases in """+country+""" are: """+str(r.json()[-1].get("Cases")))
    df = pd.json_normalize(r.json())
    layout = go.Layout(
        title = country+'\'s '+graph_type+' cases Data',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Number of cases'),)
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country))
    
    if country1 != 'یک کشور را انتخاب کنید':
        slug1 = df0.Slug[df0['Country']==country1].to_string(index=False)[1:]
        url = 'https://api.covid19api.com/total/dayone/country/'+slug1+'/status/'+graph_type
        r = requests.get(url)
        st.write("""# Total """+graph_type+""" cases in """+country1+""" are: """+str(r.json()[-1].get("Cases")))
        df = pd.json_normalize(r.json())
        layout = go.Layout(
            title = country+' vs '+country1+' '+graph_type+' cases Data',
            xaxis = dict(title = 'Date'),
            yaxis = dict(title = 'Number of cases'),)
        fig.update_layout(dict1 = layout, overwrite = True)
        fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country1))
        
    st.plotly_chart(fig, use_container_width=True)
    # url = 'https://api.covid19api.com/live/country/'+country
    # # url = 'https://api.covid19api.com/all'
    # r = requests.get(url)
    # df = json_normalize(r.json())
    df1 = df[['Country','Date','Cases','Status']]
    st.dataframe(df.sort_values(by=['Date'],ascending=False))

else:
    url = 'https://api.covid19api.com/world/total'
    r = requests.get(url)
    total = r.json()["TotalConfirmed"]
    deaths = r.json()["TotalDeaths"]
    recovered = r.json()["TotalRecovered"]
    st.write("""# Worldwide Data:""")
    st.write("Total cases: "+str(total)+", Total deaths: "+str(deaths)+", Total recovered: "+str(recovered))
    x = ["TotalCases", "TotalDeaths", "TotalRecovered"]
    y = [total, deaths, recovered]

    layout = go.Layout(
        title = 'World Data',
        xaxis = dict(title = 'Category'),
        yaxis = dict(title = 'Number of cases'),)
    
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Bar(name = 'World Data', x = x, y = y))
    st.plotly_chart(fig, use_container_width=True)

    url = 'https://api.covid19api.com/world/total'
    # url = 'https://api.covid19api.com/all'
    r = requests.get(url)
    df = pd.json_normalize(r.json())
    # df = df.rename(columns={
    #     'Lon': 'lon',
    #     'Lat': 'lat',

    #     })
    st.dataframe(df)
    # data = df[['lon','lat','Country']]
    # data.lon = data.lon.astype(float)
    # data.lat = data.lat.astype(float)
    # st.dataframe(data)
    # st.map(data)
st.sidebar.subheader(""":smile: []()""")
