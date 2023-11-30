# ruff: noqa: RUF001  # non English alphabet is used intentionally
"""
Preposition database.

Description for many useful cases
https://www.lawlessfrench.com/grammar/a-preposition/

TODO replace with data markup language.
"""

from collections.abc import Iterable, Sequence
from typing import NamedTuple, NewType

Example = str
RuExample = Example
FrExample = Example


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


data: dict[RuExample, FrExample] = {
    "Он сидит *в* кресле": "Il est assis *dans* le fauteuil",
    "Я *в* Европе": "Je suis *en* Europe",
    "Мы собираемся *в* Ниццу": "Nous allons *à* Nice",
    "бокал *для* вина": "un verre *à* vin",
    "*до* завтра": "*à* demain",
    "Я сделал это *за* пять минут": "Je l’ai fait *en* cinq minutes",
    "пить *из* стакана": "boire *dans* un verre",
    "*из* города": "*de* la ville",
    "Сделанно *из* дерева": "Fabriqué *en* bois",
    "Я иду *к* Пьеру": "Je vais *chez* Pierre",
    "Пойду *к* окну": "J'irai *à* la fenêtre",
    "Он вёл себя *как* тиран": "Il a agi *en* tyran",
    "Он *на* работе": "Il est *chez* son travail",
    "Он предпочитает путешествовать *на* поезде": "Il préfère voyager *en* train",
    "*на* пляже": "*à* la plage",
    "фильм *о* войне": "un film *de* guerre",
    "Мы были в 5 километрах *от* пляжа": "Nous sommes à 5 km *de* la plage",
    "с понедельника *по* субботу": "du lundi *au* samedi",
    "стакан *с* вином": "un verre *de* vin",
    "*с* понедельника по субботу": "*du* lundi au samedi",
    "обувь *с* высоким каблуком": "chaussures *à* talon haut",
    "Я *у* художника": "Je suis *chez* un artiste",
}


_synonyms = {
    "de": ("du",),
    "à": ("au",),
}


_synonyms_conversion = {}
for k, vals in _synonyms.items():
    for syn in vals:
        _synonyms_conversion[syn] = k


def _get_prep(text: Example) -> str:
    assert text.count("*") == 2, text  # noqa: PLR2004

    prep = text.split("*")[1]
    return _synonyms_conversion.get(prep, prep)


def get_db() -> tuple[list[Preposition], list[Relation]]:
    prepositions: set[Preposition] = set()
    relations: dict[
        tuple[Preposition, Preposition], list[tuple[RuExample, FrExample]]
    ] = {}
    for ru_example, fr_example in data.items():
        ru = _get_prep(ru_example)
        fr = _get_prep(fr_example)

        ru_prep = Preposition(RU, ru, synonyms=_synonyms.get(fr, ()))
        fr_prep = Preposition(FR, fr, synonyms=_synonyms.get(fr, ()))
        prepositions.add(ru_prep)
        prepositions.add(fr_prep)

        relations.setdefault((ru_prep, fr_prep), []).append((ru_example, fr_example))

    return sorted(prepositions, key=lambda p: (p.lang != RU, p.preposition)), [
        Relation(ru, fr, examples) for (ru, fr), examples in relations.items()
    ]


if __name__ == "__main__":
    preps, rels = get_db()
    for p in preps:
        print(p)  # noqa: T201
    print("=" * 10)  # noqa: T201
    for r in rels:
        print(r)  # noqa: T201
