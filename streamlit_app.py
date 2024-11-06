import streamlit as st
import datetime
st.title("Asmit Exercise")
@st.fragment(run_every="1s")
def auto_function():
		seconds=int(datetime.datetime.now().second)
		if seconds%5==0:
			st.write("Asmit Stand!")
		elif seconds%8==0:
			st.write("Asmit Jump!")
		elif seconds %7==0:
			st.write("Asmit Sit")
		else:
			st.write("Asmit Smile")
			
		

auto_function()
