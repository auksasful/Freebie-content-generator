


from typing_extensions import TypedDict


class Tip(TypedDict):
    name: str
    description: str
    instructions: list[str]


class TipName(TypedDict):
    name: str

class TipNames(TypedDict):
    tips: list[TipName]