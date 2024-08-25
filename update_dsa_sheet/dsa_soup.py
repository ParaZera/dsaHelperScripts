from bs4 import BeautifulSoup

from update_dsa_sheet.hero_characteristics import HeroCharacteristics


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

    def characteristics(self) -> HeroCharacteristics:
        skill_table = self._soup.find("table", class_="eigenschaften gitternetz")
        if skill_table == None:
            raise Exception("Table with class 'eigenschaften gitternetz' not found.")

        data_map: dict[str, str] = {}
        rows = skill_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols) >= 4:
                data_map[cols[0]] = int(cols[3])

        return HeroCharacteristics(data_map)

        # characteristics = {}
        # rows = self._soup.find_all("tr")
        # for row in rows:
        #     cols = row.find_all("td")
        #     cols = [ele.text.strip() for ele in cols]
        #     if len(cols) >= 2:
        #         characteristics[cols[0]] = int(cols[1])

        # return HeroCharacteristics(characteristics)
