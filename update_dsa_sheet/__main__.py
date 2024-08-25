import os
from datetime import datetime
import argparse
from .dsa_soup import DsaSoup


def back_up_input_file(file: str):
    os.rename(file, f"{file}.bak_{datetime.now().isoformat()}")


def save_modified_soup(output_file: str, soup: DsaSoup):
    with open(output_file, "w", encoding="utf8") as file:
        file.write(soup.serialize())


parser = argparse.ArgumentParser()
parser.add_argument(
    "character_sheet",
    action="store",
    type=str,
    help="Path to the character sheet",
)

args = parser.parse_args()
input_file = args.character_sheet

character_sheet = DsaSoup.from_file(input_file)
character_sheet.annotate_talents_with_characteristics_values()

back_up_input_file(input_file)
save_modified_soup(input_file, character_sheet)
