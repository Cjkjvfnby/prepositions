"""
Streamlit application that visualize relations between Russian and French prepositions.
"""
from collections import Counter

import streamlit as st
import streamlit.components.v1 as components

from prepositions._prepositions import RU, get_db
from prepositions.graph import get_preposition_graph

st.set_page_config(layout="wide")


ru_header = ":blue[Связь между русскими и французскими предлогами]"
fr_header = ":orange[La liaison entre les prépositions russes et françaises]"

st.header(f"{ru_header} / {fr_header}")


prep, relations = get_db()


def _ru_prep() -> list[str]:
    return [p.preposition for p in prep if p.lang == RU]


def _count_preposition_used(prep: str) -> str:
    counter: Counter = Counter()

    for r in relations:
        counter[r.ru.preposition] += 1
        counter[r.fr.preposition] += 1
    count = counter[prep]
    return f"{prep} ({count})"


prepositions = st.sidebar.multiselect(
    "Предлог",
    _ru_prep(),
    default=_ru_prep(),
    format_func=_count_preposition_used,
)


source_code = get_preposition_graph(
    relations, selected_prepositions=prepositions, screen_height=600
)
components.html(source_code, height=600)
