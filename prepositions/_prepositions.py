# ruff: noqa: RUF001  # non English alphabet is used intentionally
"""
Preposition database.

Description for many useful cases
https://www.lawlessfrench.com/grammar/a-preposition/

TODO replace with data markup language.
"""

from collections.abc import Iterable, Sequence
from typing import NamedTuple, NewType, TypedDict

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


class _DataItem(TypedDict):
    ru: str
    fr: str
    examples: dict[RuExample, FrExample]


data: list[_DataItem] = [
    {
        "ru": "в",
        "fr": "dans",
        "examples": {
            "Положите книги *в* коробку": "Mets les livres *dans* le carton",
            "Он сидит *в* кресле": "Il est assis *dans* le fauteuil",
            "Мы плаваем *в* бассейне": "Nous nageons *dans* la piscine",
            "Дети играют *в* саду": "Les enfants jouent *dans* le jardin",
        },
    },
    {
        "ru": "в",
        "fr": "en",
        "examples": {"Он живёт *в* Провансе": "Il habite *en* Provence"},
    },
    {
        "ru": "в",
        "fr": "à",
        "examples": {"Мы собираемся *в* Ницу": "Nous allons *à* Nice"},
    },
    {"ru": "для", "fr": "à", "examples": {"бокал *для* вина": "un verre *à* vin"}},
    {"ru": "до", "fr": "à", "examples": {"*до* завтра": "*à* demain"}},
    {
        "ru": "за",
        "fr": "dans",
        "examples": {
            "Мы едем *за* город": "Nous partons *dans* la banlieue",
            "Он спрятался *за* деревом": "Il s'est caché *dans* l'arbre",
            "Мы идем *за* реку": "Nous allons *dans* la rivière",
        },
    },
    {
        "ru": "за",
        "fr": "en",
        "examples": {"Я сделал это *за* пять минут": "Je l’ai fait *en* cinq minutes"},
    },
    {
        "ru": "из",
        "fr": "dans",
        "examples": {"пить *из* стракана": "boire *dans* un verre"},
    },
    {
        "ru": "из",
        "fr": "de",
        "examples": {"Мы прибываем *из* Лиля": "Nous arrivons *de* Lille"},
    },
    {
        "ru": "к",
        "fr": "chez",
        "examples": {
            "Я собираюсь *к* Филипу": "Je vais *chez* Philippe",
            "Я иду *к* Пьеру": "Je vais *chez* Pierre",
            "Я иду *к* парикмахеру": "Je vais *chez* le coiffeur",
        },
    },
    {"ru": "к", "fr": "à", "examples": {"пойду *к* окну": "j'irai à la fenêtre"}},
    {
        "ru": "как",
        "fr": "en",
        "examples": {"Он вёл себя *как* тиран": "Il a agi *en* tyran"},
    },
    {
        "ru": "на",
        "fr": "chez",
        "examples": {"Он *на* работе": "Il est *chez* son travail"},
    },
    {
        "ru": "на",
        "fr": "dans",
        "examples": {
            "*на* самолёте": "*dans* l’avion",
            "Он стоит *на* улице": "Il se tient debout *dans* la rue",
            "Девушка сидит *на* лавке": "La fille est assise *dans* le banc",
        },
    },
    {
        "ru": "на",
        "fr": "en",
        "examples": {
            "Он предпочитает путешествовать *на* поезде": "Il préfère voyager *en* train"
        },
    },
    {
        "ru": "по",
        "fr": "à",
        "examples": {"с понедельника *по* субботу": "du lundi *au* samedi"},
    },
    {
        "ru": "с",
        "fr": "de",
        "examples": {"суп *с* помидорами": "la soupe *de* tomates"},
    },
    {
        "ru": "с",
        "fr": "à",
        "examples": {"обувь *с* высоким каблуком": "chaussures *à* talon haut"},
    },
    {
        "ru": "у",
        "fr": "chez",
        "examples": {"Я *у* художника": "Je suis *chez* un artiste"},
    },
]


def get_db() -> tuple[list[Preposition], list[Relation]]:
    prepositions: set[Preposition] = set()
    relations: dict[
        tuple[Preposition, Preposition], list[tuple[RuExample, FrExample]]
    ] = {}
    for case in data:
        ru_prep = Preposition(RU, case["ru"])
        fr_prep = Preposition(FR, case["fr"])
        prepositions.add(ru_prep)
        prepositions.add(fr_prep)

        relations.setdefault((ru_prep, fr_prep), []).extend(case["examples"].items())

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

    # Reformat data in order
    data = sorted(data, key=lambda item: (item["ru"], item["fr"], item["examples"]))
    print(data)  # noqa: T201
