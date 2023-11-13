"""
Module to build graph with prepositions.

Utilize https://github.com/ChrisDelClea/streamlit-agraph
"""
import re
from collections.abc import Iterable
from io import StringIO

from prepositions._prepositions import (
    FR,
    RU,
    FrExample,
    Preposition,
    Relation,
    RuExample,
)

# https://docs.streamlit.io/library/api-reference/text/st.markdown
# Streamlit blue
from prepositions.network_unsafe import NetworkUnsafe


def _tuple_to_rgba(*values: int) -> str:
    r, g, b, *alpha = values
    alpha_text = f"{alpha[0]}:02x" if alpha else "FF"

    return f"#{r:02x}{g:02x}{b:02x}{alpha_text}"


# Streamlit blue
_COLOR_RU = _tuple_to_rgba(0, 104, 201)
# Streamlit orange
_COLOR_FR = _tuple_to_rgba(217, 90, 0)


def _wrap_example(example: str, color: str) -> str:
    return re.sub(r"\*(.+?)\*", rf"<b style='color:{color}'>\1</b>", example)


def _make_example_item(items: list[tuple[str, str]]) -> str:
    result = [
        "<ul>",
        *[f"<li>{_wrap_example(i, color)}</li>" for i, color in items],
        "</ul> ",
    ]

    return "".join(result)


def _make_html_example(preposition: Preposition, exam: list[tuple[str, str]]) -> str:
    if exam:
        title = f"<b>{preposition.preposition}</b>"

        if preposition.synonyms:
            title += " (" + ", ".join(preposition.synonyms) + ")"

        title += "\n"

        for ru_ex, fr_ex in exam:
            if preposition.lang == RU:
                pair = [(ru_ex, _COLOR_RU), (fr_ex, _COLOR_FR)]
            else:
                pair = [(fr_ex, _COLOR_FR), (ru_ex, _COLOR_RU)]

            title += _make_example_item(pair)

    else:
        title = ""

    return title


def get_preposition_graph(
    relations: list[Relation],
    selected_prepositions: Iterable[str],
    screen_height: int,
) -> str:
    """
    Return a graph with prepositions.
    """
    nt = NetworkUnsafe(
        height=f"{screen_height}px",
        width="100%",
        notebook=True,
        neighborhood_highlight=True,
    )
    triggered_relations = [
        r for r in relations if r.ru.preposition in selected_prepositions
    ]
    nodes_raw: dict[Preposition, list[tuple[RuExample, FrExample]]] = {}

    for relation in triggered_relations:
        nodes_raw.setdefault(relation.ru, []).extend(relation.examples)
        nodes_raw.setdefault(relation.fr, []).extend(relation.examples)

    for prep, exam in nodes_raw.items():
        title = _make_html_example(prep, exam)

        nt.add_node(
            prep.preposition,
            size=20,
            title=title,
            label="",
            shape="ellipse",
            color=_COLOR_FR if prep.lang == FR else _COLOR_RU,
        )

    for r in relations:
        title = "\n".join(
            f"{_wrap_example(ru_ex, _COLOR_RU)} / {_wrap_example(fr_ex, _COLOR_FR)}\n"
            for ru_ex, fr_ex in r.examples
        )

        nt.add_edge(r.ru.preposition, r.fr.preposition, title=title)

    return StringIO(nt.generate_html(notebook=True)).getvalue()
