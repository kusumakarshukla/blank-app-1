import streamlit as st
import datetime
st.title("My App")
@st.fragment(run_every="1s")
def auto_function():
		# This will update every 10 seconds!
		df = str(datetime.datetime.now().strftime("%d-%m-%y %h:%M:%s")
		st.write(df)

auto_function()
