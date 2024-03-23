"""Widgets."""

from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.state import SessionStateProxy


class Selector:
    """
    Preposition selector widget.
    """

    def __init__(
        self,
        parent: DeltaGenerator,
        session: SessionStateProxy,
        items: list[str],
        labels: dict[str, str],
    ):
        self._items = [(f"ru_{i}", prep) for i, prep in enumerate(items)]
        self._parent = parent
        self._session = session
        self._labels = labels
        self._set_default_values()

    def _select_all(self) -> None:
        for i, _ in enumerate(self._items):
            key = f"ru_{i}"
            self._session[key] = True

    def _deselect_all(self) -> None:
        for key, _ in self._items:
            self._session[key] = False

    def _set_default_values(self) -> None:
        for key, _ in self._items:
            if key not in self._session:
                self._session[key] = True

    def _render_widgets(self) -> None:
        col1, col2 = self._parent.columns([1, 1])

        if col1.button("Select all"):
            self._select_all()

        if col2.button("Deselect all"):
            self._deselect_all()

        for key, prep in self._items:
            toggle, label = self._parent.columns([1, 2])
            toggle.toggle(label=prep, key=key, label_visibility="collapsed")
            label.text(self._labels[prep])

    def get_selected(self) -> list[str]:
        """
        Return selected prepositions.
        """
        self._render_widgets()

        return [prep for key, prep in self._items if self._session[key]]
