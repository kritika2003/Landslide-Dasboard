import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os 
import io
import numpy as np
import altair as alt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Landslide Detection", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Landslide Detection Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.title("Crackmeter")

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    content = fl.read()
    df = pd.read_excel(io.BytesIO(content))
else:
    os.chdir(r"c:\Users\Jatin\Downloads\works")
    df = pd.read_csv("test_cracks.csv")

st.sidebar.header("Choose your filters:")

sensor_names = sorted(set(col.split('-')[0] for col in df.columns if col != 'Date Time (UTC+08:00)'))

chosen_sensor = st.sidebar.selectbox("Choose the Crackmeter", sensor_names)

data_types = [
    'Reading-Frequency (mm)',
    'Reading-Temperature (C)',
    'Reading-SignalQuality (%)'
]
selected_data_type = st.sidebar.radio("Choose the data type", data_types)

selected_column = f"{chosen_sensor}-{selected_data_type}"

filtered_data = df[[selected_column, 'Date Time (UTC+08:00)']]
filtered_data['Date Time (UTC+08:00)'] = pd.to_datetime(filtered_data['Date Time (UTC+08:00)'],format='mixed')

# Filter out values above 120000
filtered_data = filtered_data[filtered_data[selected_column] <= 120000]

plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Date Time (UTC+08:00)'], filtered_data[selected_column], marker='o', label='Data')

plt.xlabel('Date')
plt.ylabel(selected_data_type)
plt.title(f'{selected_data_type} for {chosen_sensor}')
plt.xticks(rotation=45)

plt.legend()
st.pyplot(plt)

# Plot the Altair chart
chart = alt.Chart(filtered_data).mark_point().encode(
    x='Date Time (UTC+08\:00):T',
    y=alt.Y(selected_column, title=selected_data_type),
    tooltip=[alt.Tooltip('Date Time (UTC+08\:00):T', title='Date'), alt.Tooltip(selected_column, title=selected_data_type)]
).properties(
    width=800,
    height=400
).interactive()

st.altair_chart(chart, use_container_width=True)

st.title("Tiltmeter")




df1 = pd.read_csv("test_tilts.csv")

st.sidebar.header("Choose your filters:")

tilt_names = sorted(set(col.split('-')[0] for col in df1.columns if col != 'Date Time (UTC+08:00)'))

chosen_tilt = st.sidebar.selectbox("Choose the Tiltmeter", tilt_names)

data_types = [
    'Reading-A ()',
    'Reading-B ()',
    'Reading-C ()'
]
selected_data_type = st.sidebar.radio("Choose the data type", data_types)

selected_column = f"{chosen_tilt}-{selected_data_type}"

filtered_data = df1[[selected_column, 'Date Time (UTC+08:00)']]
filtered_data['Date Time (UTC+08:00)'] = pd.to_datetime(filtered_data['Date Time (UTC+08:00)'],format='mixed')

z_scores = np.abs(stats.zscore(filtered_data[selected_column]))

filtered_data = filtered_data[(z_scores < 3)]

plt.figure(figsize=(10, 6))
plt.plot(df1['Date Time (UTC+08:00)'], df1[selected_column], marker='o', label='Data')

plt.xlabel('Date')
plt.ylabel(selected_data_type)
plt.title(f'{selected_data_type} for {chosen_tilt}')
plt.xticks(rotation=45)

plt.legend()
st.pyplot(plt)

# Plot the Altair chart
chart = alt.Chart(df1).mark_point().encode(
    x='Date Time (UTC+08\:00):T',
    y=alt.Y(selected_column, title=selected_data_type),
    tooltip=[alt.Tooltip('Date Time (UTC+08\:00):T', title='Date'), alt.Tooltip(selected_column, title=selected_data_type)]
).properties(
    width=800,
    height=400
).interactive()

st.altair_chart(chart, use_container_width=True)