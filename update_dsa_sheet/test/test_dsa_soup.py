from bs4 import BeautifulSoup
import pytest
from importlib.resources import files
from update_dsa_sheet import DsaSoup
from update_dsa_sheet.hero_characteristics import HeroCharacteristics


@pytest.fixture
def character_sheet_file_path() -> str:
    return str(
        files("update_dsa_sheet")
        .joinpath("test")
        .joinpath("test_resources")
        .joinpath("character_sheet.html")
    )


@pytest.fixture
def empty_html_document() -> str:
    return "<html></html>"


def test_dsa_soup_from_soup(empty_html_document):
    soup = BeautifulSoup(empty_html_document, "html.parser")
    assert isinstance(DsaSoup(soup), DsaSoup)


def test_dsa_soup_from_file(character_sheet_file_path):
    assert isinstance(DsaSoup.from_file(character_sheet_file_path), DsaSoup)


def test_returns_the_current_soup(empty_html_document):
    soup = BeautifulSoup(empty_html_document, "html.parser")
    dsa = DsaSoup(soup)

    assert dsa.soup == soup


def test_fetches_hero_characteristics(character_sheet_file_path):
    dsa = DsaSoup.from_file(character_sheet_file_path)
    characteristics = dsa.characteristics()
    expected = HeroCharacteristics(
        {
            "Mut": 15,
            "Klugheit": 10,
            "Intuition": 14,
            "Charisma": 8,
            "Fingerfertigkeit": 12,
            "Gewandtheit": 15,
            "Konstitution": 16,
            "Körperkraft": 15,
        }
    )

    assert characteristics == expected
