import streamlit as st
import datetime
st.title("Asmit Exercise")
@st.fragment(run_every="10s")
def auto_function():
		seconds=datetime.datetime.now().second
		if seconds%5==0:
			st.write("Asmit Stand!")
		if second%10==0:
			st.write("Asmit Jump!")
		if second %7==0:
			st.write("Asmit Sit")
			
		

auto_function()
