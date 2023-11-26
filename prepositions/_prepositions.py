# ruff: noqa: RUF001  # non English alphabet is used intentionally
"""
Preposition database.

Description for many useful cases
https://www.lawlessfrench.com/grammar/a-preposition/

TODO replace with data markup language.
"""

from collections.abc import Iterable, Sequence
from typing import NamedTuple, NewType

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


data = {
    "в": {
        "dans": {"Положите книги *в* коробку": "Mets les livres *dans* le carton"},
        "en": {"Он живёт *в* Провансе": "Il habite *en* Provence"},
        "à": {"Мы собираемся *в* Ницу": "Nous allons *à* Nice"},
    },
    "для": {"à": {"бокал *для* вина": "un verre *à* vin"}},
    "до": {"à": {"*до* завтра": "*à* demain"}},
    "за": {"en": {"Я сделал это *за* пять минут": "Je l’ai fait *en* cinq minutes"}},
    "из": {
        "dans": {"пить *из* стракана": "boire *dans* un verre"},
        "de": {"Мы прибываем *из* Лиля": "Nous arrivons *de* Lille"},
    },
    "к": {"à": {"пойду *к* окну": "j'irai à la fenêtre"}},
    "как": {"en": {"Он вёл себя *как* тиран": "Il a agi *en* tyran"}},
    "на": {
        "dans": {"*на* самолёте": "*dans* l’avion"},
        "en": {
            "Он предпочитает путешествовать *на* поезде": "Il préfère voyager *en* train",
        },
    },
    "по": {"à": {"с понедельника *по* субботу": "du lundi *au* samedi"}},
    "с": {
        "de": {"суп *с* помидорами": "la soupe *de* tomates"},
        "à": {"обувь *с* высоким каблуком": "chaussures *à* talon haut"},
    },
}


def get_db() -> tuple[list[Preposition], list[Relation]]:
    prepositions = []
    relations = []
    for ru, related in data.items():
        ru_prep = Preposition(RU, ru)
        prepositions.append(ru_prep)
        for fr, example in related.items():
            fr_prep = Preposition(FR, fr)
            prepositions.append(fr_prep)

            relations.append(Relation(ru_prep, fr_prep, tuple(example.items())))
    return prepositions, relations
