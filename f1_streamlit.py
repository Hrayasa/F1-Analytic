import os
import streamlit as st
import fastf1 as ff1
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup cache for faster data loading
if not os.path.exists('cache'):
    os.makedirs('cache')
ff1.Cache.enable_cache('cache')

# Streamlit App Title
st.title("Formula 1 Race Insights")

# Sidebar for user input
season = st.sidebar.selectbox("Pick a Season", range(2018, 2024))
race = st.sidebar.selectbox("Choose a Race", ff1.get_event_schedule(season)['EventName'].tolist())

# Trigger analysis when the button is pressed
if st.sidebar.button("Show me the data!"):
    try:
        # Load up the race data
        race_session = ff1.get_session(season, race, 'R')
        race_session.load()
        laps = race_session.laps

        # Clean up the lap time data
        laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
        laps = laps.dropna(subset=['LapTimeSeconds'])

        # 1. Average Lap Times
        st.subheader("How Fast Were They, on Average?")
        avg_lap_times = laps.groupby('Driver')['LapTimeSeconds'].mean().sort_values()
        fig_avg, ax_avg = plt.subplots()
        sns.barplot(x=avg_lap_times.values, y=avg_lap_times.index, ax=ax_avg)
        st.pyplot(fig_avg)

        # 2. Driver Positions Throughout the Race
        st.subheader("Where Did They Finish?")
        fig_pos, ax_pos = plt.subplots(figsize=(14, 8))
        for driver in laps['Driver'].unique():
            driver_laps = laps[laps['Driver'] == driver].sort_values(by='LapNumber')
            ax_pos.plot(driver_laps['LapNumber'], driver_laps['Position'], label=driver)
        ax_pos.invert_yaxis()
        ax_pos.legend()
        st.pyplot(fig_pos)

        # 3. Fastest Lap Times
        st.subheader("Who Had the Quickest Lap?")
        fastest_laps = laps.groupby('Driver')['LapTimeSeconds'].min().sort_values()
        fig_fast, ax_fast = plt.subplots()
        sns.barplot(x=fastest_laps.values, y=fastest_laps.index, ax=ax_fast)
        st.pyplot(fig_fast)

    except Exception as e:
        st.error(f"Oops! Something went wrong: {e}")





'''
TO RUN THE PROGRAM, YOU CAN EITHER OPEN THE TERMINAL AND WHERE THE FILE IS PRESENT OR OPEN AND INTERGRATED TERMINAL 
The enter the command 

                                        streamlit run f1_streamlit.py
'''