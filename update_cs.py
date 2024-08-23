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


def generate_titel_row(soup):
    th1 = soup.new_tag("th", attrs={"class": "titel", "colspan": "2"})
    th1.append("Meta-Talente")

    tr1 = soup.new_tag("tr")
    tr1.append(th1)

    return tr1


def generate_left_row(soup):
    th_name = soup.new_tag("th", attrs={"class": "name", "colspan": "2"})
    th_name.append("Meta-Talente")

    th_taw = soup.new_tag("th", attrs={"class": "taw"})
    th_taw.append("TAW")

    tr_head = soup.new_tag("tr")
    tr_head.append(th_name)
    tr_head.append(th_taw)

    td_name = soup.new_tag("td", attrs={"class": "name"})
    td_name.append("I AM NAME")

    td_probe = soup.new_tag("td", attrs={"class": "probe"})
    td_probe.append("I AM PROBE")

    td_taw = soup.new_tag("td", attrs={"class": "taw"})
    td_taw.append("TAW")

    tr1 = soup.new_tag("tr")
    tr1.append(td_name)
    tr1.append(td_probe)
    tr1.append(td_taw)

    td_name2 = soup.new_tag("td", attrs={"class": "name"})
    td_name2.append("I AM NAME 2")

    td_probe2 = soup.new_tag("td", attrs={"class": "probe"})
    td_probe2.append("I AM PROBE 2")

    td_taw2 = soup.new_tag("td", attrs={"class": "taw"})
    td_taw2.append("99")

    tr2 = soup.new_tag("tr")
    tr2.append(td_name2)
    tr2.append(td_probe2)
    tr2.append(td_taw2)

    tbody = soup.new_tag("tbody")
    tbody.append(tr_head)
    tbody.append(tr1)
    tbody.append(tr2)

    table = soup.new_tag("table", attrs={"class": "talentgruppe gitternetz"})
    table.append(tbody)

    div = soup.new_tag("div", attrs={"class": "links_innen"})
    div.append(table)

    td_links = soup.new_tag("td", attrs={"class": "links"})
    td_links.append(div)

    return td_links

    # tr_upper = soup.new_tag("tr")
    # tr_upper.append(td_links)

    # return tr_upper


def generate_right_row(soup):
    th_name = soup.new_tag("th", attrs={"class": "name", "colspan": "2"})
    th_name.append("Meta-Talente")

    th_taw = soup.new_tag("th", attrs={"class": "taw"})
    th_taw.append("TAW")

    tr_head = soup.new_tag("tr")
    tr_head.append(th_name)
    tr_head.append(th_taw)

    td_name = soup.new_tag("td", attrs={"class": "name"})
    td_name.append("I AM NAME")

    td_probe = soup.new_tag("td", attrs={"class": "probe"})
    td_probe.append("I AM PROBE")

    td_taw = soup.new_tag("td", attrs={"class": "taw"})
    td_taw.append("TAW")

    tr1 = soup.new_tag("tr")
    tr1.append(td_name)
    tr1.append(td_probe)
    tr1.append(td_taw)

    td_name2 = soup.new_tag("td", attrs={"class": "name"})
    td_name2.append("I AM NAME 2")

    td_probe2 = soup.new_tag("td", attrs={"class": "probe"})
    td_probe2.append("I AM PROBE 2")

    td_taw2 = soup.new_tag("td", attrs={"class": "taw"})
    td_taw2.append("99")

    tr2 = soup.new_tag("tr")
    tr2.append(td_name2)
    tr2.append(td_probe2)
    tr2.append(td_taw2)

    tbody = soup.new_tag("tbody")
    tbody.append(tr_head)
    tbody.append(tr1)
    tbody.append(tr2)

    table = soup.new_tag("table", attrs={"class": "talentgruppe gitternetz"})
    table.append(tbody)

    div = soup.new_tag("div", attrs={"class": "rechts_innen"})
    div.append(table)

    td_links = soup.new_tag("td", attrs={"class": "rechts"})
    td_links.append(div)

    return td_links

    # tr_upper = soup.new_tag("tr")
    # tr_upper.append(td_links)

    # return tr_upper


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

    meta_talents_table.append(tbody)

    tr1_titel = generate_titel_row(soup)
    tbody.append(tr1_titel)

    tr2_body = soup.new_tag("tr")
    left = generate_left_row(soup)
    right = generate_right_row(soup)

    tr2_body.append(left)
    tr2_body.append(right)
    tbody.append(tr2_body)

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

    skill_values = extract_skill_values(soup)
    apply_modification(skill_values, soup)
    rename_input_file(html_file)
    save_modified_file(html_file, soup)


if __name__ == "__main__":
    main()
