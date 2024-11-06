import streamlit as st
import datetime
@st.fragment(run_every="1s")
def auto_function():
		seconds=int(datetime.datetime.now().second)
		if seconds%5==0:
			st.title("Asmit Stand!")
		elif seconds%8==0:
			st.title("Asmit Jump!")
		elif seconds %7==0:
			st.title("Asmit Sit")
		else:
			st.title("Asmit Smile")
			
		

auto_function()
