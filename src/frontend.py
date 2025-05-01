
import streamlit as st

from src.load_events import *

if 'mun' not in st.session_state:
    st.session_state.mun = ""
if 'tour' not in st.session_state:
    st.session_state.tour = ""

st.title("Get Events")
st.subheader("")

col1, col2 = st.columns(2)

with col1:
    if st.button("Event loader (Municipality)",type="primary"):
        st.session_state.mun = get_events_lan()
    st.caption(st.session_state.mun)

with col2:
    if st.button("Event loader (Tourism)",type="primary"):
        st.session_state.tour = get_events_tour()
    st.caption(st.session_state.tour)
