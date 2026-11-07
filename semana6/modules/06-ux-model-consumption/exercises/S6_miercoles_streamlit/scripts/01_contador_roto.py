# Vuelve a ejecutar desde 0 el fichero
import streamlit as st
st.title("Contador sin memoria")
count = 0
if st.button("Sumar"):
    count += 1
st.metric("Cuenta", count)
