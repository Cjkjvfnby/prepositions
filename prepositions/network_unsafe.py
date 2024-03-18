"""
Workaround that pyvis does not support HTML in title.

https://github.com/WestHealth/pyvis/issues/144

Implementation is based on this sample:
https://visjs.github.io/vis-network/examples/network/other/html-in-titles.html


This is not universal fix, only methods that are used in my code are patched.
"""

from hashlib import md5
from typing import Any

from pyvis.network import Network
from pyvis.node import Node


class NetworkUnsafe(Network):
    """
    Wrapper for Network, with fix HTML in title.
    """

    def add_edge(self, source: Node, to: Node, **options: Any) -> None:
        """Wrap Network.add_edge."""
        if options["title"]:
            title = options["title"].replace("\n", "<br>")
            options["title"] = self.__get_edge_title(title)
        super().add_edge(source, to, **options)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.__placeholder: dict[str, str] = {}

    def __get_node_title(self, html: str) -> str:
        key = md5(html.encode()).hexdigest()  # noqa: S324
        self.__placeholder[key] = html
        return key

    def __get_edge_title(self, html: str) -> str:
        key = md5(html.encode()).hexdigest()  # noqa: S324
        self.__placeholder[key] = html
        return key

    def add_node(
        self,
        n_id: str | int,
        label: str | None = None,
        shape: str = "dot",
        color: str = "#97c2fc",
        **options: Any,
    ) -> None:
        """Wrap Network.add_node."""
        if options["title"]:
            title = options["title"].replace("\n", "<br>")
            options["title"] = self.__get_node_title(title)
        super().add_node(n_id, label, shape, color, **options)

    def generate_html(
        self,
        name: str = "index.html",
        local: bool = True,  # noqa: FBT002, FBT001
        notebook: bool = False,  # noqa: FBT002, FBT001
    ) -> str:
        """Wrap Network.generate_html."""
        source_code = super().generate_html(name, local, notebook)

        source_code = source_code.replace(
            "// initialize global variables.",
            """

        function htmlTitle(html) {
          const container = document.createElement("div");
          container.innerHTML = html;
          return container;
        };

        """,
        )

        for k, v in self.__placeholder.items():
            source_code = source_code.replace(f'"{k}"', f'htmlTitle("{v}")')

        return source_code
