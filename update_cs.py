#!/bin/env python3

import os
from bs4 import BeautifulSoup, ResultSet, Tag
from datetime import datetime
import argparse

shorthand_map: dict[str, str] = {
    "MU": "Mut",
    "KL": "Klugheit",
    "IN": "Intuition",
    "CH": "Charisma",
    "FF": "Fingerfertigkeit",
    "GE": "Gewandtheit",
    "KO": "Konstitution",
    "KK": "Körperkraft",
    "GS": "Geschwindigkeit",
}

reversed_shorthand_map = {v: k for k, v in shorthand_map.items()}


class SkillValues:
    _data_map: dict[str, int] = None

    def __init__(self, soup: BeautifulSoup):
        skill_table = soup.find("table", class_="eigenschaften gitternetz")
        if skill_table == None:
            raise Exception("Table with class 'eigenschaften gitternetz' not found.")

        data_map = {}
        rows = skill_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols) >= 4:
                key = cols[0]
                value = cols[3]

                data_map[key] = value
                data_map[reversed_shorthand_map[key]] = value

        self._data_map = data_map

    def __getitem__(self, key: str) -> int:
        return self._data_map[key]


class MetaTalent:
    _name: str = None
    _skill_values: SkillValues = None
    _skills: list[str] = None

    def __init__(self, name: str, skill_values: SkillValues, used_skills: list[str]):
        self._name = name
        self._skill_values = skill_values
        self._skills = used_skills

    def name(self) -> str:
        return self._name

    def probe(self) -> str:

        short_skills = [
            reversed_shorthand_map[skill] if len(skill) > 2 else skill
            for skill in self._skills
        ]

        short_skills = sorted(short_skills)
        skill_values = [self._skill_values[skill] for skill in short_skills]
        zipped = zip(short_skills, skill_values)

        strings = [f"{skill}[{value}]" for (skill, value) in zipped]
        probe = "+".join(strings)

        return probe

    def taw(self) -> str:
        values = [self._skill_values[skill] for skill in self._skills]
        sum = sum(values)
        quotient = sum // len(values)

        return quotient


class TalentSoup:
    soup = None

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def generate_headline(self, headline: str) -> Tag:
        th_name = self.soup.new_tag("th", attrs={"class": "titel", "colspan": "2"})
        th_name.append(headline)

        tr_head = self.soup.new_tag("tr")
        tr_head.append(th_name)

        return tr_head

    def _generate_column_headline(self, headline: str) -> Tag:
        th_name = self.soup.new_tag("th", attrs={"class": "name", "colspan": "2"})
        th_name.append(headline)

        th_taw = self.soup.new_tag("th", attrs={"class": "taw"})
        th_taw.append("TAW")

        tr_head = self.soup.new_tag("tr")
        tr_head.append(th_name)
        tr_head.append(th_taw)

        return tr_head

    def generate_table_entry(self, talent: MetaTalent):
        td_name = self.soup.new_tag("td", attrs={"class": "name"})
        td_name.append(talent.name())

        td_probe = self.soup.new_tag("td", attrs={"class": "probe"})
        td_probe.append(talent.probe())

        td_taw = self.soup.new_tag("td", attrs={"class": "taw"})
        td_taw.append(talent.taw())

        tr = self.soup.new_tag("tr")
        tr.append(td_name)
        tr.append(td_probe)
        tr.append(td_taw)

        return tr

    def generate_column(
        self, headline: str, column_name: str, talents: list[MetaTalent]
    ):
        tbody = self.soup.new_tag("tbody")

        tr_head = self._generate_column_headline(headline)
        tbody.append(tr_head)

        for talent in talents:
            tr = self.generate_table_entry(talent)
            tbody.append(tr)

        table = self.soup.new_tag("table", attrs={"class": "talentgruppe gitternetz"})
        table.append(tbody)

        div = self.soup.new_tag("div", attrs={"class": f"{column_name}_innen"})
        div.append(table)

        td = self.soup.new_tag("td", attrs={"class": column_name})
        td.append(div)

        return td


def extract_skill_values(soup):
    skill_table = soup.find("table", class_="eigenschaften gitternetz")
    if skill_table == None:
        raise Exception("Table with class 'eigenschaften gitternetz' not found.")

    data_map = {}
    rows = skill_table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if len(cols) >= 4:
            data_map[cols[0]] = cols[3]
    return data_map


def modify_cell_content(skill_values: dict[str, str], cell: Tag) -> str:
    for shorthand, full_name in shorthand_map.items():
        cell.string = cell.string.replace(
            shorthand, f" {shorthand}[{skill_values[full_name]}] "
        )
    # replace space with non-breaking space
    cell.string = cell.string.replace(" ", "\u00A0")

    return cell.string


def apply_modification(skill_values: dict[str, str], soup):
    tables: ResultSet[Tag] = soup.find_all("table", class_="talentgruppe gitternetz")
    for table in tables:
        rows: ResultSet[Tag] = table.find_all("tr")
        for row in rows:
            cols: ResultSet[Tag] = row.find_all("td")
            for col in cols:
                if col.has_attr("class") and "probe" in col["class"]:
                    modified_cell: str = modify_cell_content(skill_values, col)
                    col.string = modified_cell

    table = soup.find("table", class_="talente")
    meta_talents_table = soup.new_tag("table", attrs={"class": "talente"})
    table.insert_after(meta_talents_table)

    tbody = soup.new_tag("tbody")

    meta_talents_left = [
        MetaTalent("I AM NAME", "I AM PROBE", "TAW"),
        MetaTalent("I AM NAME 2", "I AM PROBE 2", "99"),
    ]

    meta_talents_right = [
        MetaTalent("I AM NAME", "I AM PROBE", "000"),
        MetaTalent("I AM NAME 2", "I AM PROBE 2", "100"),
    ]

    talent_soup = TalentSoup(soup)
    headline = talent_soup.generate_headline("Meta-Talente")
    left_row = talent_soup.generate_column("Test Headline", "links", meta_talents_left)
    right_row = talent_soup.generate_column(
        "Test Headline", "rechts", meta_talents_right
    )

    tbody.append(headline)
    tbody.append(left_row)
    tbody.append(right_row)

    meta_talents_table.append(tbody)


def rename_input_file(input_file: str):
    os.rename(input_file, f"{input_file}.bak_{datetime.now().isoformat()}")


def save_modified_file(output_file: str, soup):
    with open(output_file, "w") as file:
        file.write(soup.prettify(formatter=None))


def main():
    parser = argparse.ArgumentParser(
        description="Add feature values to talent descriptions."
    )
    parser.add_argument("file", help="HTML file to modify")
    args = parser.parse_args()

    html_file = args.file
    with open(html_file, "r") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")

    skill_values = SkillValues(soup)
    # skill_values = extract_skill_values(soup)
    apply_modification(skill_values, soup)
    rename_input_file(html_file)
    save_modified_file(html_file, soup)


if __name__ == "__main__":
    main()
