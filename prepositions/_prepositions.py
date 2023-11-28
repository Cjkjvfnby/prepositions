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
            "Он сидит *в* кресле": "Il est assis *dans* le fauteuil",
        },
    },
    {
        "ru": "в",
        "fr": "de",
        "examples": {
            "*в* городе": "*de* la ville",
        },
    },
    {
        "ru": "в",
        "fr": "en",
        "examples": {
            "*в* театре": "*en* théâtre",
        },
    },
    {
        "ru": "в",
        "fr": "à",
        "examples": {
            "Мы собираемся *в* Ниццу": "Nous allons *à* Nice",
        },
    },
    {"ru": "для", "fr": "à", "examples": {"бокал *для* вина": "un verre *à* vin"}},
    {"ru": "до", "fr": "à", "examples": {"*до* завтра": "*à* demain"}},
    {
        "ru": "за",
        "fr": "dans",
        "examples": {
            "мы идем *за* реку": "nous allons *dans* la rivière",
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
        "examples": {"пить *из* стакана": "boire *dans* un verre"},
    },
    {
        "ru": "из",
        "fr": "de",
        "examples": {
            "*из* дома": "*De* la maison",
        },
    },
    {
        "ru": "к",
        "fr": "chez",
        "examples": {
            "Я иду *к* Пьеру": "Je vais *chez* Pierre",
        },
    },
    {
        "ru": "к",
        "fr": "à",
        "examples": {
            "пойду *к* окну": "j'irai à la fenêtre",
        },
    },
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
            "Девушка сидит *на* лавке": "La fille est assise *dans* le banc",
        },
    },
    {
        "ru": "на",
        "fr": "en",
        "examples": {
            "Он предпочитает путешествовать *на* поезде": "Il préfère voyager *en* train",
        },
    },
    {
        "ru": "на",
        "fr": "à",
        "examples": {
            "*на* пляже": "*À* la plage",
        },
    },
    {
        "ru": "по",
        "fr": "en",
        "examples": {
            "*по* дороге": "*En* route",
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


"""
Chat GPT promt example


Для французского предлога de найди мне варианты использования, которые переводятся на русский предложением с предлогом.
В переводе обязательно должна быть часть речи предлог, если его нет, то такой пример не подходит.

Нужно найти все возможные русские предлоги которые переводятся с заданного французского.
Пример должны быть отличными друг от друга, один пример для каждого русского предлога.

Результат должен быть оформлен в виде списка на языке Python с форматированием для удобства чтения.
Все элементы должны иметь хвостовую запятую запятую.

Каждый элемент списка это словарь с тремя ключами.

"ru" со значением русского предлога из перевода
"fr" со значенем французского предлога
"examples" словарь с примерами.  Где русский пример является ключом, а французский перевод значением.
Каждая пара ключ значение должна быть на новой строке.

В примерах нужно убрать точки и предлог обрамить звёздочками.


"""

_synonyms = {
    "de": ("du",),
    "à": ("au",),
}


def get_db() -> tuple[list[Preposition], list[Relation]]:
    prepositions: set[Preposition] = set()
    relations: dict[
        tuple[Preposition, Preposition], list[tuple[RuExample, FrExample]]
    ] = {}
    for case in data:
        ru_prep = Preposition(RU, case["ru"])
        fr_prep = Preposition(FR, case["fr"], synonyms=_synonyms.get(case["fr"], ()))
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
    data = sorted(
        data, key=lambda item: (item["ru"], item["fr"], tuple(item["examples"].keys()))
    )

    deduplicated: dict[tuple[str, str], dict[RuExample, FrExample]] = {}
    for item in data:
        ru, fr, examples = item["ru"], item["fr"], item["examples"]
        deduplicated.setdefault((ru, fr), {}).update(examples)

    data = [
        {"ru": ru, "fr": fr, "examples": examples}
        for (ru, fr), examples in deduplicated.items()
    ]

    data = sorted(
        data, key=lambda item: (item["ru"], item["fr"], tuple(item["examples"].keys()))
    )

    print(data)  # noqa: T201
