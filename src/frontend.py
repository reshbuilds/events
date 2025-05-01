
import streamlit as st

from src.load_events import *

st.title("Get Events")
st.subheader("")

if st.button("Event loader (Jönköping)",type="primary"):
    st.caption(get_events_jkpg())

