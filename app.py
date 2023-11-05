"""
Streamlit application that visualize relations between Russian and French prepositions.
"""
import streamlit as st  # noqa: F401

from prepositions.graph import get_preposition_graph

get_preposition_graph()
