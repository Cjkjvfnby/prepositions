"""
Module to build graph with prepositions.

Utilize https://github.com/ChrisDelClea/streamlit-agraph
"""
from collections.abc import Sequence
from typing import Any

from streamlit_agraph import Config, Edge, Node, agraph

from prepositions._icons import icon_from_text
from prepositions._prepositions import (
    FrExample,
    Lang,
    Preposition,
    RuExample,
    relations,
)

# Sky Blue #89ABE3
_COLOR_RU = (0x89, 0xAB, 0xE3)
# Bubblegum Pink #EA738D
_COLOR_FR = (0xEA, 0x73, 0x8D)


def _make_node(
    prep: Preposition,
    examples: Sequence[tuple[RuExample, FrExample]],
) -> Node:
    kwargs = {
        "id": prep.preposition,
        "size": 25,
        "shape": "circularImage",
        "color": "#0FF0000",
    }

    if examples:
        text = f"{prep.preposition}\n\n"

        for ru_ex, fr_ex in examples:
            if prep.lang == prep.lang == Lang.RU:
                text += f"{ru_ex} / {fr_ex}\n"
            else:
                text += f"{fr_ex} / {ru_ex}\n"
        kwargs["title"] = text

    kwargs["image"] = icon_from_text(
        prep.preposition,
        _COLOR_RU if prep.lang == Lang.RU else _COLOR_FR,
    )

    return Node(**kwargs)


def get_preposition_graph() -> Any:
    """
    Return a graph with prepositions.
    """
    config = Config(
        height=800,
        width=700,
        nodeHighlightBehavior=True,
        highlightColor="#000000",
        directed=False,
        collapsible=True,
    )

    nodes_raw: dict[Preposition, list[tuple[RuExample, FrExample]]] = {}

    for relation in relations:
        nodes_raw.setdefault(relation.ru, []).extend(relation.examples)
        nodes_raw.setdefault(relation.fr, []).extend(relation.examples)

    return agraph(
        nodes=[_make_node(prep, exam) for prep, exam in nodes_raw.items()],
        edges=[
            Edge(
                title="\n".join(f"{ru_ex} / {fr_ex}\n" for ru_ex, fr_ex in r.examples),
                source=r.ru.preposition,
                label="",
                target=r.fr.preposition,
            )
            for r in relations
        ],
        config=config,
    )
