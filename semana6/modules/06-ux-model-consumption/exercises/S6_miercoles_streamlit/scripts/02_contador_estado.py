import streamlit as st
st.title("Contador con estado")
if "count" not in st.session_state:
    #session_state pierde la informacion si se hace un reset de la pagina
    st.session_state.count = 0
if st.button("Sumar"):
    st.session_state.count += 1
st.metric("Cuenta", st.session_state.count)
