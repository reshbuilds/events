
import streamlit as st

from src.load_events import *

if 'gov' not in st.session_state:
    st.session_state.gov = ""
if 'priv' not in st.session_state:
    st.session_state.priv = ""

st.title("Get Events")
st.subheader("")

col1, col2 = st.columns(2)

with col1:
    if st.button("Event loader (Municipality)",type="primary"):
        st.session_state.gov = get_events_gov()
    st.caption(st.session_state.gov)

with col2:
    if st.button("Event loader (Private)",type="primary"):
        st.session_state.priv = get_events_private()
    st.caption(st.session_state.priv)
