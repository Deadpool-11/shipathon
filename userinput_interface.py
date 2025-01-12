import streamlit as st
import pandas as pd

st.set_page_config(page_title="User Input Interface", page_icon="📝", layout="wide")

st.markdown('<h1 class="centered-title">Input Your Event Data</h1>', unsafe_allow_html=True)

priority_index = st.text_input("Priority Index")
event_type = st.text_input("Event Type")
description = st.text_input("Description")
time = st.text_input("Time (24-hour format)")
link = st.text_input("Link")
date = st.text_input("Date (YYYY-MM-DD)")

# Button to navigate to the basic interface
if st.button("Go to Calendar"):
    data = {
        "Priority index": [priority_index],
        "Type": [event_type],
        "Description": [description],
        "Time": [time],
        "Link": [link],
        "Date": [date]
    }
    df = pd.DataFrame(data)
    
    # Save the data to a CSV file
    df.to_csv("user_input.csv", index=False)
    
    st.success("Data submitted successfully!")
    
    # Navigate to the basic interface
    st.write("[go to the 'EventConnect' page](pages/basic_frontend.py) to view your calendar.")