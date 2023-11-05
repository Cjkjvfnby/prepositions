# ruff: noqa: F401, RUF001  # non English alphabet is used intentionally
"""
Preposition database.

Description for many useful cases
https://www.lawlessfrench.com/grammar/a-preposition/

TODO replace with data markup language.
"""

from collections.abc import Sequence
from enum import Enum, auto
from typing import NamedTuple

RuExample = str
FrExample = str


class Lang(Enum):
    RU = auto()
    FR = auto()


class Preposition(NamedTuple):
    lang: Lang
    preposition: str


class Relation(NamedTuple):
    ru: Preposition
    fr: Preposition
    examples: Sequence[tuple[RuExample, FrExample]]


def _relations(
    ru: Preposition,
    fr: Preposition,
    *examples: tuple[RuExample, FrExample],
) -> Relation:
    return Relation(ru, fr, examples)


в = Preposition(Lang.RU, "в")
на = Preposition(Lang.RU, "на")
к = Preposition(Lang.RU, "к")
с = Preposition(Lang.RU, "с")
до = Preposition(Lang.RU, "до")
по = Preposition(Lang.RU, "по")
для = Preposition(Lang.RU, "для")
из = Preposition(Lang.RU, "из")
за = Preposition(Lang.RU, "за")
за = Preposition(Lang.RU, "за")
как = Preposition(Lang.RU, "как")


à = Preposition(Lang.FR, "à")
dans = Preposition(Lang.FR, "dans")
en = Preposition(Lang.FR, "en")


relations = [
    _relations(в, à, ("Мы собираемся в Ницу", "Nous allons à Nice")),
    _relations(в, dans, ("Положите книги в коробку", "Mets les livres dans le carton")),
    _relations(в, en, ("Он живёт в Провансе", "Il habite en Provence")),
    _relations(до, à, ("до завтра", "à demain")),
    _relations(по, à, ("с понедельника по субботу", "du lundi au samedi")),
    _relations(для, à, ("бокал для вина", "un verre à vin")),
    _relations(с, à, ("обувь с высоким каблуком", "chaussures à talon haut")),
    _relations(на, dans, ("на самолёте", "dans l’avion")),
    _relations(из, dans, ("пить из стракана", "boire dans un verre")),
    _relations(за, en, ("Я сделал это за пять минут", "Je l’ai fait en cinq minutes")),
    _relations(
        на,
        en,
        ("Он предпочитает путешествовать на поезде", "Il préfère voyager en train"),
    ),
    _relations(как, en, ("Он вёл себя как тиран", "Il a agi en tyran.")),
]
