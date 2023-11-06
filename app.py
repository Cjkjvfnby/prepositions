"""
Streamlit application that visualize relations between Russian and French prepositions.
"""
import streamlit as st

from prepositions._prepositions import Preposition, ru_map, ru_prepositions
from prepositions.graph import get_preposition_graph

ru_header = ":blue[Связь между русскими и французскими предлогами]"
fr_header = ":orange[La liaison entre les prépositions russes et françaises]"

st.header(f"{ru_header} / {fr_header}")


def _count_preposition_used(prep: Preposition) -> str:
    count = len(ru_map.get(prep, []))
    return f"{prep.preposition} ({count})"


prepositions = st.sidebar.multiselect(
    "Предлог",
    ru_prepositions,
    default=ru_prepositions,
    format_func=_count_preposition_used,
)


get_preposition_graph(prepositions, 700, 800)
