from typing import Optional

from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag

from update_dsa_sheet.catppuccin import DEFAULT_ACCENT, generate_css
from update_dsa_sheet.hero_characteristics import HeroCharacteristics

NBSP = "\u00A0"


class DsaSoup:
    _soup: BeautifulSoup = None

    def __init__(self, character_sheet: BeautifulSoup):
        self._soup = character_sheet

    @classmethod
    def from_file(cls, character_sheet_file: str):
        with open(character_sheet_file, "r", encoding="utf8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")

        return cls(soup)

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    def serialize(self) -> str:
        return self._soup.prettify(formatter=None)

    def apply_theme(self, theme_name: str, accent: str = DEFAULT_ACCENT) -> None:
        css = generate_css(theme_name, accent)
        self._inject_style(css)

    def _inject_style(self, css: str) -> None:
        head = self._soup.find("head")
        if head is None:
            head = Tag(name="head")
            if self._soup.html:
                self._soup.html.insert(0, head)
        style_tag = Tag(name="style")
        style_tag["type"] = "text/css"
        style_tag.append(NavigableString(css))
        head.append(style_tag)

    def characteristics(self) -> HeroCharacteristics:
        skill_table = self._soup.find("table", class_="eigenschaften gitternetz")
        if skill_table is None:
            raise KeyError("Table with class 'eigenschaften gitternetz' not found.")

        data_map = self._parse_characteristics_table(skill_table)
        return HeroCharacteristics(data_map)

    @staticmethod
    def _parse_characteristics_table(table: Tag) -> dict[str, int]:
        data_map: dict[str, int] = {}
        for row in table.find_all("tr"):
            cols = [col.text.strip() for col in row.find_all("td")]
            if len(cols) >= 4:
                data_map[cols[0]] = int(cols[3])
        return data_map

    @staticmethod
    def _strip_whitespace(text: str) -> str:
        return text.replace(" ", "").replace(NBSP, "")

    @staticmethod
    def _annotate_shorthand(text: str, characteristics: HeroCharacteristics) -> str:
        for shorthand in characteristics.keys():
            annotated = f"{NBSP}{shorthand}[{characteristics[shorthand]:02}]{NBSP}"
            text = text.replace(shorthand, annotated)
        return text

    def _modify_cell_content(
        self, characteristics: HeroCharacteristics, cell: Tag
    ) -> str:
        text = self._strip_whitespace(cell.string)
        return self._annotate_shorthand(text, characteristics)

    def annotate_talents_with_characteristics_values(
        self, characteristics: Optional[HeroCharacteristics] = None
    ):
        characteristics = (
            self.characteristics() if characteristics is None else characteristics
        )

        for cell in self._find_probe_cells():
            cell.string = self._modify_cell_content(characteristics, cell)

    def _find_probe_cells(self) -> list[Tag]:
        cells = []
        tables: ResultSet[Tag] = self.soup.find_all(
            "table", class_="talentgruppe gitternetz"
        )
        for table in tables:
            for row in table.find_all("tr"):
                for col in row.find_all("td"):
                    if col.has_attr("class") and "probe" in col["class"]:
                        cells.append(col)
        return cells
