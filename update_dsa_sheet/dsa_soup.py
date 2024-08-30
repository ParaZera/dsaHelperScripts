from typing import Optional
from bs4 import BeautifulSoup, ResultSet, Tag
from update_dsa_sheet.hero_characteristics import HeroCharacteristics
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.meta_talent_group import MetaTalentGroup
from update_dsa_sheet.meta_talent_soup import MetaTalentSoup
from update_dsa_sheet.talents import Talents


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

    def talents(self) -> Talents:
        tables: ResultSet[Tag] = self.soup.find_all(
            "table", class_="talentgruppe gitternetz"
        )

        talents: dict[str, int] = {}

        for table in tables:
            rows: ResultSet[Tag] = table.find_all("tr")
            for row in rows:
                cols: ResultSet[Tag] = row.find_all("td")
                name: str = None
                taw: int = None

                for col in cols:
                    if col.has_attr("class") and "name" in col["class"]:
                        name = col.string.strip()

                    if col.has_attr("class") and "taw" in col["class"]:
                        try:
                            taw = int(col.string.strip())
                        except ValueError:
                            pass

                if name is not None and taw is not None:
                    talents[name] = taw

        return Talents(talents)

    def _header(self, headline: str) -> Tag:
        header_name = Tag(name="th", attrs={"colspan": "2", "class": "titel"})
        header_name.string = headline

        root = Tag(name="tr")
        root.append(header_name)
        return root

    def _table_outline(self, prefix: str, child: Tag) -> Tag:
        div_tag = Tag(name="div", attrs={"class": f"{prefix}_innen"})
        div_tag.append(child)

        table_data_cell = Tag(name="td", attrs={"class": f"{prefix}"})
        table_data_cell.append(div_tag)

        return table_data_cell

        root = Tag(name="tr")
        root.append(table_data_cell)
        return root

    def add_meta_talents(self, meta_talents: list[MetaTalentGroup]):
        g = MetaTalentGroup(
            "Meta Talent Group",
            [
                MetaTalent("Meta Talent 1", ["Talent1", "Talent2"]),
                MetaTalent("Meta Talent 2", ["Talent3", "Talent4"]),
            ],
        )

        s = MetaTalentSoup(g)

        ########################

        root_tbody = Tag(name="tbody")
        root_tbody.append(self._header("Meta-Talente"))
        ########################
        left = self._table_outline("links", child=s.to_soup())
        right = self._table_outline("rechts", child=s.to_soup())

        root_tr = Tag(name="tr")
        root_tr.append(left)
        root_tr.append(right)

        root_tbody.append(root_tr)

        ###########

        root_table = Tag(name="table", attrs={"class": "talente"})
        root_table.append(root_tbody)

        ############
        root: Tag = self.soup.find_all("table", class_="talente")[0]
        root.append(root_table)

        # s = MetaTalentSoup(meta_talents[0])
        # ss = s.to_soup()

        # links
        # ltr = Tag(name="tr")
        # ltd1 = Tag(name="td", attrs={"class": "links"})
        # ltr.append(ltd1)
        # ltdiv = Tag(name="div", attrs={"class": "links_innen"})

        # # ltdiv.append(ss)

        # ltd1.append(ltdiv)

        # links ende

        # ltdiv.append(ss)

        a = root_table.prettify(formatter=None)

        print("HELLO")
        print(a)

        print("HELLO")
        pass
