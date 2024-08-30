from bs4 import Tag
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.meta_talent_group import MetaTalentGroup


class MetaTalentSoup:
    _talents: MetaTalentGroup = None

    def __init__(self, talents: MetaTalentGroup):
        self._talents = talents

    def to_soup(self) -> Tag:
        root = Tag(name="table", attrs={"class": "talentgruppe-gitternetz"})
        tbody = Tag(name="tbody")

        header = Tag(name="tr")
        header_name = Tag(name="th", attrs={"class": "name", "colspan": "2"})
        header_name.string = self._talents._name

        header_taw = Tag(name="th", attrs={"class": "taw"})
        header_taw.string = "TaW"

        header.append(header_name)
        header.append(header_taw)

        tbody.append(header)

        # for talent in self._talents.talents:
        #     tr = Tag(name="tr")
        #     td = Tag(name="td")
        #     td.string = talent.name
        #     tr.append(td)
        #     td = Tag(name="td")
        #     for t in talent.talents:
        #         td.string = t
        #         tr.append(td)
        #     tbody.append(tr)

        root.append(tbody)

        return root
