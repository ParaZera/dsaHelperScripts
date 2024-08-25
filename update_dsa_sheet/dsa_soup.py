from typing import Optional
from bs4 import BeautifulSoup, ResultSet, Tag
from update_dsa_sheet.hero_characteristics import HeroCharacteristics


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

    def characteristics(self) -> HeroCharacteristics:
        skill_table = self._soup.find("table", class_="eigenschaften gitternetz")
        if skill_table is None:
            raise KeyError("Table with class 'eigenschaften gitternetz' not found.")

        data_map: dict[str, str] = {}
        rows = skill_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols) >= 4:
                data_map[cols[0]] = int(cols[3])

        return HeroCharacteristics(data_map)

    def _modify_cell_content(
        self, characteristics: HeroCharacteristics, cell: Tag
    ) -> str:
        s = cell.string
        s = s.replace(" ", "")
        s = s.replace("\u00A0", "")
        for shorthand in characteristics.keys():
            s = s.replace(
                shorthand, f"\u00A0{shorthand}[{characteristics[shorthand]:02}]\u00A0"
            )
        # replace space with non-breaking space
        # cell.string = cell.string.replace(" ", "\u00A0")

        return s

    def annotate_talents_with_characteristics_values(
        self, characteristics: Optional[HeroCharacteristics] = None
    ):
        characteristics = (
            self.characteristics() if characteristics is None else characteristics
        )

        tables: ResultSet[Tag] = self.soup.find_all(
            "table", class_="talentgruppe gitternetz"
        )
        for table in tables:
            rows: ResultSet[Tag] = table.find_all("tr")
            for row in rows:
                cols: ResultSet[Tag] = row.find_all("td")
                for col in cols:
                    if col.has_attr("class") and "probe" in col["class"]:
                        modified_cell: str = self._modify_cell_content(
                            characteristics, col
                        )
                        col.string = modified_cell
