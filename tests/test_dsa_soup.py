from __future__ import annotations

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from update_dsa_sheet.dsa_soup import DsaSoup
from update_dsa_sheet.hero_characteristics import HeroCharacteristics


@pytest.fixture(name="empty_html_document")
def fixture_empty_html_document() -> str:
    return "<html></html>"


@pytest.fixture(name="character_sheet_file_path")
def fixture_character_sheet_file_path(resources_dir: Path) -> str:
    return str(resources_dir / "character_sheet.html")


@pytest.fixture(name="custom_characteristics")
def fixture_custom_characteristics() -> HeroCharacteristics:
    return HeroCharacteristics(
        {
            "Mut": 1,
            "Klugheit": 2,
            "Intuition": 3,
            "Charisma": 4,
            "Fingerfertigkeit": 5,
            "Gewandtheit": 6,
            "Konstitution": 7,
            "Körperkraft": 8,
        }
    )


def test_dsa_soup_from_soup(empty_html_document: str):
    soup = BeautifulSoup(empty_html_document, "html.parser")
    assert isinstance(DsaSoup(soup), DsaSoup)


def test_dsa_soup_from_file(character_sheet_file_path: str):
    assert isinstance(DsaSoup.from_file(character_sheet_file_path), DsaSoup)


def test_returns_the_current_soup(empty_html_document: str):
    soup = BeautifulSoup(empty_html_document, "html.parser")
    dsa = DsaSoup(soup)
    assert dsa.soup == soup


def test_fetches_hero_characteristics(character_sheet_file_path: str):
    dsa = DsaSoup.from_file(character_sheet_file_path)
    characteristics = dsa.characteristics()

    expected = HeroCharacteristics(
        {
            "Mut": 15,
            "Klugheit": 10,
            "Intuition": 14,
            "Charisma": 8,
            "Fingerfertigkeit": 12,
            "Gewandtheit": 14,
            "Konstitution": 16,
            "Körperkraft": 15,
        }
    )
    assert characteristics == expected


@pytest.mark.parametrize(
    "expected_file, custom",
    [
        ("characteristics_and_talents_annotated.html", None),
        ("characteristics_and_talents_annotated_custom.html", "use_custom"),
    ],
)
def test_annotation_of_talents_with_characteristics(
    load_soup,
    expected_file: str,
    custom: str | None,
    custom_characteristics: HeroCharacteristics,
):
    dsa = DsaSoup(load_soup("characteristics_and_talents.html"))

    if custom:
        dsa.annotate_talents_with_characteristics_values(custom_characteristics)
    else:
        dsa.annotate_talents_with_characteristics_values()

    actual = dsa.soup.prettify(formatter=None)
    expected = load_soup(expected_file).prettify(formatter=None)

    assert actual == expected
