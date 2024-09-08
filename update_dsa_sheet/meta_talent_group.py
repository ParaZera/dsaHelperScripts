from typing import Any

from bs4 import Tag
import yaml
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.talents import Talents


class MetaTalentGroup:
    _name: str = None
    _meta_talents: list[MetaTalent] = None

    def __init__(self, name: str, talents: list[MetaTalent]):
        self._name = name
        self._meta_talents = talents

    def __repr__(self) -> str:
        return f"MetaTalentGroup(name: {self._name}, talents: {self._meta_talents})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MetaTalentGroup):
            return False
        return self.to_dict() == other.to_dict()

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        data = {k.lower(): v for k, v in data.items()}
        talents = [MetaTalent.from_dict(t) for t in data["talents"]]
        return MetaTalentGroup(data["name"], talents)

    def to_dict(self) -> dict[str, Any]:
        talents = [t.to_dict() for t in self._meta_talents]
        return {"name": self._name, "talents": talents}

    @classmethod
    def from_yaml(cls, yaml_str: str):
        y: dict[str, Any] = yaml.load(yaml_str, Loader=yaml.FullLoader)
        y: dict[str, Any] = {k.lower(): v for k, v in y.items()}
        talents = [MetaTalent.from_dict(t) for t in y["talents"]]
        return MetaTalentGroup(y["name"], talents)

    def to_yaml(self) -> str:
        d = self.to_dict()
        return yaml.dump(d)

    @property
    def talents(self) -> list[MetaTalent]:
        return self._meta_talents

    @property
    def name(self) -> str:
        return self._name

    def _soup_header(self) -> Tag:
        header_name = Tag(name="th", attrs={"class": "name"})
        header_name.string = self._name

        header_formula = Tag(name="th", attrs={"class": "formel"})
        header_formula.string = "Formel"

        header_taw = Tag(name="th", attrs={"class": "taw"})
        header_taw.string = "TaW"

        root = Tag(name="tr")
        root.append(header_name)
        root.append(header_formula)
        root.append(header_taw)

        return root

    def to_soup(self, talents: Talents) -> Tag:
        table: Tag = Tag(name="table", attrs={"class": "talentgruppe gitternetz"})
        tbody: Tag = Tag(name="tbody")

        table.append(tbody)
        tbody.append(self._soup_header())

        for meta_talent in self._meta_talents:
            m = meta_talent.to_soup(talents)
            tbody.append(m)

        return table
