from bs4 import BeautifulSoup
import pytest
from importlib.resources import files
from update_dsa_sheet.dsa_soup import DsaSoup
from update_dsa_sheet.hero_characteristics import HeroCharacteristics
from update_dsa_sheet.talents import Talents


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


@pytest.fixture
def character_sheet_talents() -> Talents:
    return Talents(
        {
            "dolche": 2,
            "hiebwaffen": 6,
            "raufen": 7,
            "ringen": 6,
            "säbel": 0,
            "speere": 4,
            "wurfmesser": 0,
            "wurfspeere": 4,
            "zweihandhiebwaffen": 1,
            #
            "athletik": 7,
            "klettern": 3,
            "körperbeherrschung": 5,
            "schleichen": 4,
            "schwimmen": 2,
            "selbstbeherrschung": 3,
            "sich verstecken": 2,
            "singen": 0,
            "sinnenschärfe": 6,
            "tanzen": 0,
            "zechen": 1,
            #
            "menschenkenntnis": 1,
            "überreden": 1,
            #
            "fährtensuchen": 8,
            "fallen stellen": 3,
            "fischen/angeln": 2,
            "orientierung": 5,
            "wettervorhersage": 4,
            "wildnisleben": 8,
            #
            "götter und kulte": 2,
            "pflanzenkunde": 3,
            "rechnen": 0,
            "sagen und legenden": 3,
            "tierkunde": 3,
            #
            "alaani": 4,
            "garethi": 2,
            "ologhaijan": 6,
            "thorwalsch": 8,
            #
            "gjalskisch": 0,
            #
            "abrichten": 3,
            "feuersteinbearbeitung": 3,
            "gerber/kürschner": 4,
            "heilkunde: wunden": 4,
            "holzbearbeitung": 4,
            "kochen": 0,
            "lederarbeiten": 3,
            "malen/zeichnen": 0,
            "schneidern": 0,
            #
            "ritualkenntnis: durro-dûn": 3,
        }
    )


def test_talents_temp(character_sheet_file_path, character_sheet_talents):
    dsa = DsaSoup.from_file(character_sheet_file_path)
    talents = dsa.talents()
    print(talents)
    print("")
    print(character_sheet_talents)
    assert character_sheet_talents == talents

    # assert False
