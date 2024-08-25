from bs4 import BeautifulSoup
import pytest
from importlib.resources import files
from update_dsa_sheet.dsa_soup import DsaSoup
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


@pytest.fixture
def characteristics_and_talents_sheet_soup() -> BeautifulSoup:
    path = str(
        files("update_dsa_sheet")
        .joinpath("test")
        .joinpath("test_resources")
        .joinpath("characteristics_and_talents.html")
    )

    with open(path, "r", encoding="utf8") as file:
        html_content = file.read()
    return BeautifulSoup(html_content, "html.parser")


@pytest.fixture
def characteristics_and_talents_annotated_sheet_soup() -> BeautifulSoup:
    path = str(
        files("update_dsa_sheet")
        .joinpath("test")
        .joinpath("test_resources")
        .joinpath("characteristics_and_talents_annotated.html")
    )

    with open(path, "r", encoding="utf8") as file:
        html_content = file.read()
    return BeautifulSoup(html_content, "html.parser")


@pytest.fixture
def characteristics_and_talents_custom_annotated_sheet_soup() -> BeautifulSoup:
    path = str(
        files("update_dsa_sheet")
        .joinpath("test")
        .joinpath("test_resources")
        .joinpath("characteristics_and_talents_annotated_custom.html")
    )

    with open(path, "r", encoding="utf8") as file:
        html_content = file.read()
    return BeautifulSoup(html_content, "html.parser")


@pytest.fixture
def custom_characteristics() -> HeroCharacteristics:
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
            "Gewandtheit": 14,
            "Konstitution": 16,
            "Körperkraft": 15,
        }
    )

    assert characteristics == expected


def test_annotation_of_talents_with_characteristics(
    characteristics_and_talents_sheet_soup,
    characteristics_and_talents_annotated_sheet_soup,
):
    dsa = DsaSoup(characteristics_and_talents_sheet_soup)
    dsa.annotate_talents_with_characteristics_values()
    dsa = dsa.soup.prettify(formatter=None)

    expected = characteristics_and_talents_annotated_sheet_soup.prettify(formatter=None)

    assert dsa == expected


def test_annotation_of_talents_with_custom_characteristics(
    characteristics_and_talents_sheet_soup,
    custom_characteristics,
    characteristics_and_talents_custom_annotated_sheet_soup,
):
    dsa = DsaSoup(characteristics_and_talents_sheet_soup)
    dsa.annotate_talents_with_characteristics_values(custom_characteristics)
    dsa = dsa.soup.prettify(formatter=None)

    expected = characteristics_and_talents_custom_annotated_sheet_soup.prettify(
        formatter=None
    )

    assert dsa == expected
