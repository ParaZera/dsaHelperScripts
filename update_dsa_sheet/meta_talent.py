from typing import Any
import yaml


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


class MetaTalentGroup:
    _name: str = None
    _talents: list[MetaTalent] = None

    def __init__(self, name: str, talents: list[MetaTalent]):
        self._name = name
        self._talents = talents

    def __repr__(self) -> str:
        return f"MetaTalentGroup(name: {self._name}, talents: {self._talents})"

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
        return {"name": self._name, "talents": self._talents}
