#!/bin/env python3

import os
import sys
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
    meta_talents_table = soup.new_tag("table", class_="talente")
    table.insert_after(meta_talents_table)

    th1 = soup.new_tag("th", class_="titel", colspan="2")
    th1.append("Meta-Talente")

    tr1 = soup.new_tag("tr")
    tr1.append(th1)

    div_links_innen = soup.new_tag("div", class_="links_innen")
    td_links = soup.new_tag("td", class_="links")
    td_links.append(div_links_innen)

    div_rechts_innen = soup.new_tag("div", class_="rechts_innen")
    td_rechts = soup.new_tag("td", class_="rechts")
    td_rechts.append(div_rechts_innen)

    tr2 = soup.new_tag("tr")
    tr2.append(td_links)
    tr2.append(td_rechts)

    tbody = soup.new_tag("tbody")
    tbody.append(tr1)

    meta_talents_table.append(tbody)

    # tbody = soup.new_tag("tbody")
    # tr1 = tbody.append("tr")
    # tr1.append("td").append("th", class_="titel", colspan="2").append("Meta-Talente")

    # tr1 = tbody.append("tr")
    # tr1.append("td").append("th", class_="titel", colspan="2").append("Meta-Talente")


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

    skill_values = extract_skill_values(soup)
    apply_modification(skill_values, soup)
    rename_input_file(html_file)
    save_modified_file(html_file, soup)


if __name__ == "__main__":
    main()
