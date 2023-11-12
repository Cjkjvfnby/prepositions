# ruff: noqa: F401, RUF001  # non English alphabet is used intentionally
"""
Preposition database.

Description for many useful cases
https://www.lawlessfrench.com/grammar/a-preposition/

TODO replace with data markup language.
"""

from collections.abc import Iterable, Sequence
from typing import Any, NamedTuple, NewType

RuExample = str
FrExample = str


Lang = NewType("Lang", str)

RU = Lang("RU")
FR = Lang("FR")


class Preposition(NamedTuple):
    lang: Lang
    preposition: str
    synonyms: Iterable[str] = ()

    def __str__(self):
        return self.preposition

    def __ne__(self, other: object):
        return not self.__eq__(other)


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


def get_db() -> tuple[list[Preposition], list[Relation]]:
    в = Preposition(RU, "в")
    на = Preposition(RU, "на")
    к = Preposition(RU, "к")
    с = Preposition(RU, "с")
    до = Preposition(RU, "до")
    по = Preposition(RU, "по")
    для = Preposition(RU, "для")
    из = Preposition(RU, "из")
    за = Preposition(RU, "за")
    как = Preposition(RU, "как")

    à = Preposition(FR, "à", ("au",))
    dans = Preposition(FR, "dans")
    en = Preposition(FR, "en")
    de = Preposition(FR, "de")

    relations = [
        _relations(в, à, ("Мы собираемся *в* Ницу", "Nous allons *à* Nice")),
        _relations(
            в, dans, ("Положите книги *в* коробку", "Mets les livres *dans* le carton")
        ),
        _relations(в, en, ("Он живёт *в* Провансе", "Il habite *en* Provence")),
        _relations(до, à, ("*до* завтра", "*à* demain")),
        _relations(по, à, ("с понедельника *по* субботу", "du lundi *au* samedi")),
        _relations(для, à, ("бокал *для* вина", "un verre *à* vin")),
        _relations(с, à, ("обувь *с* высоким каблуком", "chaussures *à* talon haut")),
        _relations(на, dans, ("*на* самолёте", "*dans* l’avion")),
        _relations(из, dans, ("пить *из* стракана", "boire *dans* un verre")),
        _relations(
            за, en, ("Я сделал это *за* пять минут", "Je l’ai fait *en* cinq minutes")
        ),
        _relations(
            на,
            en,
            (
                "Он предпочитает путешествовать *на* поезде",
                "Il préfère voyager *en* train",
            ),
        ),
        _relations(как, en, ("Он вёл себя *как* тиран", "Il a agi *en* tyran")),
        _relations(к, à, ("пойду *к* окну", "j'irai à la fenêtre")),
        _relations(из, de, ("Мы прибываем *из* Лиля", "Nous arrivons *de* Lille")),
        _relations(с, de, ("суп *с* помидорами", "la soupe *de* tomates")),
    ]

    return [в, на, к, с, до, по, для, из, за, как, à, dans, en, de], relations
