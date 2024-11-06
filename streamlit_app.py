import streamlit as st
import datetime
st.title("Asmit Exercise")
@st.fragment(run_every="1s")
def auto_function():
		seconds=int(datetime.datetime.now().second)
		if seconds%5==0:
			st.write("Asmit Stand!")
		if seconds%10==0:
			st.write("Asmit Jump!")
		if seconds %7==0:
			st.write("Asmit Sit")
			
		

auto_function()
