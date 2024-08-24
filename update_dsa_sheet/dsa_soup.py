from bs4 import BeautifulSoup


class DsaSoup:
    _soup: BeautifulSoup = None

    def __init__(self, character_sheet: BeautifulSoup):
        self._soup = character_sheet

    @classmethod
    def from_file(cls, character_sheet_file: str):
        with open(character_sheet_file, "r") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")

        return cls(soup)

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup
