class Talents:
    _talents: dict[str, int]

    def __init__(self, talents: dict[str, int]):
        self._talents = {k.lower(): v for k, v in talents}

    def __getitem__(self, key: str) -> int:
        return self._talents[key.lower()]

    def __repr__(self) -> str:
        return f"Talents({self._talents})"
