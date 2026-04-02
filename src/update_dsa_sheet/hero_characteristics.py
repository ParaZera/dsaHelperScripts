_shorthand_map = {
    "charisma": "ch",
    "fingerfertigkeit": "ff",
    "gewandtheit": "ge",
    "intuition": "in",
    "klugheit": "kl",
    "konstitution": "ko",
    "körperkraft": "kk",
    "mut": "mu",
}

_longhand_map = {v: k for k, v in _shorthand_map.items()}


def _normalize_key(key: str) -> str:
    lower = key.lower()
    if lower in _longhand_map:
        return lower
    if lower in _shorthand_map:
        return _shorthand_map[lower]
    raise KeyError(f"Unknown characteristic: {key}")


class HeroCharacteristics:
    _values: dict[str, int]

    def __init__(self, characteristics: dict[str, int]):
        self._values = {}
        for key, value in characteristics.items():
            try:
                shorthand = _normalize_key(key)
            except KeyError:
                continue
            self._values[shorthand] = value

    def keys(self) -> set[str]:
        return {k.upper() for k in _longhand_map}

    def __getitem__(self, key: str) -> int:
        return self._values[_normalize_key(key)]

    def __getattr__(self, name: str) -> int:
        attr = name.rstrip("_")
        if attr in _longhand_map:
            return self._values.get(attr)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HeroCharacteristics):
            return False
        return self._values == other._values

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __repr__(self) -> str:
        return f"HeroCharacteristics({self._values})"

    def __str__(self) -> str:
        return repr(self)
