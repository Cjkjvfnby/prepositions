"""
Streamlit application that visualize relations between Russian and French prepositions.
"""

from collections import Counter
from collections.abc import Iterator

import streamlit as st
import streamlit.components.v1 as components

from prepositions._prepositions import RU, Relation, get_db
from prepositions.graph import get_preposition_graph
from prepositions.widgets.selector import Selector

st.set_page_config(layout="wide")

ru_header = ":blue[Связь между русскими и французскими предлогами]"
fr_header = ":orange[La liaison entre les prépositions russes et françaises]"

st.header(f"{ru_header} / {fr_header}")


def _get_preposition_labels(
    relations: list[Relation], prepositions: list[str]
) -> Iterator[tuple[str, str]]:
    for prep in prepositions:
        counter: Counter = Counter()
        for r in relations:
            counter[r.ru.preposition] += 1
            counter[r.fr.preposition] += 1
        count = counter[prep]
        yield prep, f"{prep}({count})"


prep, relations = st.cache_data(get_db)()


@st.cache_data
def _get_selector_data() -> tuple[list[str], dict[str, str]]:
    russian_prepositions_ = sorted({p.preposition for p in prep if p.lang == RU})
    labels_ = dict(_get_preposition_labels(relations, russian_prepositions_))
    return russian_prepositions_, labels_


russian_prepositions, labels = _get_selector_data()

selector = Selector(st.sidebar, st.session_state, russian_prepositions, labels)

prepositions = selector.get_selected()

value = st.sidebar.slider(
    "height",
    key="screen_height",
    min_value=500,
    max_value=1000,
    value=600,
    step=50,
    help="Screen height",
)

source_code = get_preposition_graph(
    relations, selected_prepositions=prepositions, screen_height=value
)

components.html(source_code, height=value)
