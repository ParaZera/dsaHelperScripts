from __future__ import annotations

import argparse
import os
from datetime import datetime

from .catppuccin import ACCENT_COLORS, DEFAULT_ACCENT, VALID_THEMES
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
    parser.add_argument(
        "--theme",
        type=str,
        choices=VALID_THEMES,
        default=None,
        help="Apply a Catppuccin color theme (e.g. mocha, latte, frappe, macchiato)",
    )
    parser.add_argument(
        "--theme-accent",
        type=str,
        choices=ACCENT_COLORS,
        default=DEFAULT_ACCENT,
        help=f"Accent color for the theme (default: {DEFAULT_ACCENT})",
    )
    args = parser.parse_args(argv)

    input_file = args.character_sheet
    character_sheet = DsaSoup.from_file(input_file)
    character_sheet.annotate_talents_with_characteristics_values()

    if args.theme:
        character_sheet.apply_theme(args.theme, accent=args.theme_accent)

    back_up_input_file(input_file)
    save_modified_soup(input_file, character_sheet)
    return 0
