import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
from io import BytesIO
from readtxt import convert_to_df, datetime_range, generate_datetime, final_df

st.set_page_config(layout="wide")

st.title("Visulization of Wind Speed and Wind Direction")
st.markdown('A Web App by Suiyuan Team')
st.markdown("")
#st.markdown(f'<p style=color:#0066cc;font-size:22px;border-radius:2%;">{"Hey there! Welcome to my app. This app lets the user entering the name of"the station and will be able to retrieve the wind speed and wind direction at that station for the past 45 days togerther with forecasting how wind speed and direction will change in the next 72 hours. And after entering the date the app will show the polar plot of the daily average wind speed in the mean direction of that day.**Give it a go!**"}</p>', unsafe_allow_html=True)
st.markdown("Hey there! Welcome to my app. This app lets the user entering the name of"
			" the station and will be able to retrieve the wind speed and wind direction"
			" at that station for the past 45 days togerther with forecasting how wind"
			" speed and direction will change in the next 72 hours. And after entering"
			" the date the app will show the polar plot of the daily average wind speed"
			" in the mean direction of that day.**Give it a go!**")


with st.sidebar:
    #st.write("Here you can choose station and select date.")
    st.markdown(f'<p style=color:#0066cc;font-size:22px;border-radius:2%;">{"Here you can choose station and select date."}</p>', unsafe_allow_html=True)
    station = st.selectbox("Select your station: ",('KIKT Station', 'KAPT Station', 'KMIS Station'))
    st.write('You selected:', station)

    d = st.date_input("Select your data", datetime.date(2021, 12, 2))
    st.write('Your selected data is:', d)

st.markdown("")

if station == 'KIKT Station':
	target_url = 'https://www.ndbc.noaa.gov/data/realtime2/KIKT.txt'
elif station == 'KAPT Station':
	target_url = 'https://www.ndbc.noaa.gov/data/realtime2/KBQX.txt'
else:
	target_url = 'https://www.ndbc.noaa.gov/data/realtime2/KMIS.txt'
	
df = final_df(target_url)

st.title('Wind Speed and Wind Direction at that station for the past 45 days')

st.subheader('Wind Direction')
st.line_chart(df['WDIR'])
st.subheader('Wind Speed')
st.line_chart(df['WSPD'])

st.title('Forecast of wind speed and direction in the next 72 hours')
df['daytime']= pd.to_datetime(df['date']).dt.date
df_day = df[df['daytime']==d]

if df_day.shape[0] == 0:
	st.error('Error: The date you enter is not in the dataset.')
else:
	st.subheader('Forecast of Wind Direction')

	st.subheader('Forecast of Wind Speed')
	
	
st.title('Daily average wind speed in the mean direction of the day you selected.')
width = st.sidebar.slider("plot width", 0.1, 25., 3.)
height = st.sidebar.slider("plot height", 0.1, 25., 1.)
if df_day.shape[0] == 0:
	st.error('Error: The date you enter is not in the dataset.')
else:
	mean_dir = df_day['WDIR'].mean()
	mean_spd = df_day['WSPD'].mean()
	
	fig = plt.figure(figsize = (width,height))
	ax = fig.add_subplot(polar = True)
	plt.grid(True)
	
	ax.set_theta_offset(np.pi/2)
	ax.set_theta_direction(-1)
	ax.set_rlabel_position(0)
	ax.set_rlim(0,15)
	ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
	
	ax.plot(mean_dir/180.*np.pi, mean_spd, marker='o',color='r')
	plt.annotate('('+str(round(mean_spd,2))+', '+str(round(mean_dir,2))+')', xy = (mean_dir/180.*np.pi, mean_spd),color='red')
	ax.arrow(0, 0, mean_dir/180.*np.pi, mean_spd,edgecolor = 'red', facecolor = 'red')

	st.pyplot(fig,figsize=(1, 1))
    #buf = BytesIO()
    #fig.savefig(buf, format="png")
    #st.image(buf)