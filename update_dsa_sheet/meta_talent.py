from typing import Any
from bs4 import Tag
import yaml

from update_dsa_sheet.talents import Talents


class MetaTalent:
    _name: str = None
    _talents: list[str] = None

    def __init__(self, name: str, talents: list[str]):
        self._name = name
        self._talents = talents

    def __repr__(self) -> str:
        return f"MetaTalent(name: {self._name}, talents: {self._talents})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MetaTalent):
            return False
        return self.to_dict() == other.to_dict()

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        data = {k.lower(): v for k, v in data.items()}
        return MetaTalent(data["name"], data["talents"])

    def to_dict(self) -> dict[str, Any]:
        return {"name": self._name, "talents": self._talents}

    @classmethod
    def from_yaml(cls, yaml_str: str):
        y: dict[str, Any] = yaml.load(yaml_str, Loader=yaml.FullLoader)
        y: dict[str, Any] = {k.lower(): v for k, v in y.items()}

        return MetaTalent(y["name"], y["talents"])

    def to_yaml(self) -> str:
        d = self.to_dict()
        return yaml.dump(d)

    def _get_taw(self, talents: Talents) -> int:
        missing_talents = [
            t for t in self._talents if talents.get(t, default=None) is None
        ]

        if len(missing_talents) > 0:
            return "Fehlende Talente: " + ", ".join(missing_talents)

        taw_sum = sum([talents.get(v, default=0) for v in self._talents])
        taw = taw_sum // len(self._talents)
        return taw

    def to_soup(self, talents: Talents) -> Tag:
        if len(self._talents) == 0:
            raise Exception()
            # raise RuntimeError(f"Meta Talent {self._name} has no talent values")
        row: Tag = Tag(name="tr")
        name: Tag = Tag(name="td", attrs={"class": "name"})
        name.string = self._name

        formula: Tag = Tag(name="td", attrs={"class": "formel"})
        formula.string = f"({" + ".join(self._talents)}) / {len(self._talents)}"
        taw: Tag = Tag(name="td", attrs={"class": "taw"})
        taw.string = str(self._get_taw(talents))

        row.append(name)
        row.append(formula)
        row.append(taw)

        return row
