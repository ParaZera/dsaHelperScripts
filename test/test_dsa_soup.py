from bs4 import BeautifulSoup
import pytest
from importlib.resources import files
from update_dsa_sheet import DsaSoup


@pytest.fixture
def character_sheet_file_path() -> str:
    return str(
        files("test").joinpath("test_resources").joinpath("character_sheet.html")
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
