from __future__ import annotations

import argparse
import os
from datetime import datetime

from .dsa_soup import DsaSoup


def back_up_input_file(file: str) -> None:
    os.rename(file, f"{file}.bak_{datetime.now().isoformat()}")


def save_modified_soup(output_file: str, soup: DsaSoup) -> None:
    with open(output_file, "w", encoding="utf8") as file:
        file.write(soup.serialize())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="update-dsa-sheet")
    parser.add_argument(
        "character_sheet",
        type=str,
        help="Path to the character sheet",
    )
    args = parser.parse_args(argv)

    input_file = args.character_sheet
    character_sheet = DsaSoup.from_file(input_file)
    character_sheet.annotate_talents_with_characteristics_values()

    back_up_input_file(input_file)
    save_modified_soup(input_file, character_sheet)
    return 0
