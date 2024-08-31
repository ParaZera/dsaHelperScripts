from typing import Optional


class Talents:
    _talents: dict[str, int]

    def __init__(self, talents_dict: dict[str, int]):
        self._talents = {k.lower(): v for k, v in talents_dict.items()}

    def __getitem__(self, key: str) -> int:
        return self._talents[key.lower()]

    def __repr__(self) -> str:
        return f"Talents({self._talents})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Talents):
            return False

        return self._talents == value._talents

    def get(self, key: str, default: Optional[int] = None) -> int:
        return self._talents.get(key.lower(), default)
