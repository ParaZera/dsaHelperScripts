import pytest

from update_dsa_sheet.hero_characteristics import HeroCharacteristics


@pytest.fixture
def shorthand_characteristics():
    return {
        "cH": 1,
        "ff": 2,
        "Ge": 3,
        "in": 4,
        "KK": 5,
        "KL": 6,
        "ko": 7,
        "mu": 8,
        "zz": 99,
    }


@pytest.fixture
def longhand_characteristics():
    return {
        "CHARISMA": 11,
        "FINgerfertigKEIT": 12,
        "GEWANDTHEIT": 13,
        "INTUITION": 14,
        "körperkraft": 15,
        "KLUGHEIT": 16,
        "KONSTITUTION": 17,
        "MUT": 18,
        "Geschwindigkeit": 1,
    }


def test_from_shorthand_keys(shorthand_characteristics):
    hero = HeroCharacteristics(shorthand_characteristics)

    assert hero.ch == 1
    assert hero.ff == 2
    assert hero.ge == 3
    assert hero.in_ == 4
    assert hero.kk == 5
    assert hero.kl == 6
    assert hero.ko == 7
    assert hero.mu == 8

    assert hero["ch"] == 1
    assert hero["FF"] == 2
    assert hero["ge"] == 3
    assert hero["in"] == 4
    assert hero["Kk"] == 5
    assert hero["kL"] == 6
    assert hero["ko"] == 7
    assert hero["mu"] == 8


def test_from_longhand_keys(longhand_characteristics):
    hero = HeroCharacteristics(longhand_characteristics)

    assert hero.ch == 11
    assert hero.ff == 12
    assert hero.ge == 13
    assert hero.in_ == 14
    assert hero.kk == 15
    assert hero.kl == 16
    assert hero.ko == 17
    assert hero.mu == 18

    assert hero["ch"] == 11
    assert hero["FF"] == 12
    assert hero["gE"] == 13
    assert hero["In"] == 14
    assert hero["kk"] == 15
    assert hero["kl"] == 16
    assert hero["ko"] == 17
    assert hero["mu"] == 18


def test_characteristics_keys(shorthand_characteristics):
    hero = HeroCharacteristics(shorthand_characteristics)

    assert set(hero.keys()) == {
        "CH",
        "FF",
        "GE",
        "IN",
        "KK",
        "KL",
        "KO",
        "MU",
    }
