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


class HeroCharacteristics:
    _ch: int = None
    _ff: int = None
    _ge: int = None
    _in: int = None
    _kl: int = None
    _ko: int = None
    _kk: int = None
    _mu: int = None

    def __init__(self, characteristics: dict[str, int]):
        dict = {
            k: v
            for k, v in characteristics.items()
            if k.lower() in _shorthand_map.keys() or k.lower() in _longhand_map.keys()
        }

        dict = {
            (
                k.lower()
                if k.lower() in _shorthand_map.values()
                else _shorthand_map[k.lower()]
            ): v
            for k, v in dict.items()
        }

        self._ch = dict.get("ch")
        self._ff = dict.get("ff")
        self._ge = dict.get("ge")
        self._in = dict.get("in")
        self._kl = dict.get("kl")
        self._ko = dict.get("ko")
        self._kk = dict.get("kk")
        self._mu = dict.get("mu")

    def __getitem__(self, key: str) -> int:
        k = (
            key.lower()
            if key.lower() in _shorthand_map.values()
            else _shorthand_map[key.lower()]
        )

        return getattr(self, f"_{k}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HeroCharacteristics):
            return False

        return all(
            getattr(self, f"_{k}") == getattr(other, f"_{k}")
            for k in _shorthand_map.values()
        )

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __repr__(self) -> str:
        characteristics = {k: getattr(self, f"_{k}") for k in _shorthand_map.values()}
        return f"HeroCharacteristics({characteristics})"

    @property
    def ch(self) -> int:
        return self._ch

    @property
    def ff(self) -> int:
        return self._ff

    @property
    def ge(self) -> int:
        return self._ge

    @property
    def in_(self) -> int:
        return self._in

    @property
    def kl(self) -> int:
        return self._kl

    @property
    def ko(self) -> int:
        return self._ko

    @property
    def kk(self) -> int:
        return self._kk

    @property
    def mu(self) -> int:
        return self._mu
