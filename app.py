"""
Streamlit application that visualize relations between Russian and French prepositions.
"""
import streamlit as st

from prepositions.graph import get_preposition_graph

ru_header = ":blue[Связь между русскими и французскими предлогами]"
fr_header = ":orange[La liaison entre les prépositions russes et françaises]"

st.header(f"{ru_header} / {fr_header}")

get_preposition_graph()
