import os
from datetime import datetime
import argparse

from .meta_talent import MetaTalent
from .dsa_soup import DsaSoup


# def back_up_input_file(file: str):
#     os.rename(file, f"{file}.bak_{datetime.now().isoformat()}")


# def save_modified_soup(output_file: str, soup: DsaSoup):
#     with open(output_file, "w", encoding="utf8") as file:
#         file.write(soup.serialize())


# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "character_sheet",
#     action="store",
#     type=str,
#     help="Path to the character sheet",
# )

# parser.add_argument(
#     "-m",
#     "--meta-talents",
#     action="store",
#     type=str,
#     help="Path to the meta-talents file",
# )

# args = parser.parse_args()
# input_file = args.character_sheet
# meta_talents_file = args.meta_talents
# add_meta_talents = meta_talents_file is not None

# character_sheet = DsaSoup.from_file(input_file)
# character_sheet.annotate_talents_with_characteristics_values()

# if add_meta_talents:
#     character_sheet.annotate_talents_with_meta_talents(meta_talents_file)

# back_up_input_file(input_file)
# save_modified_soup(input_file, character_sheet)


meta_talent = MetaTalent("test", ["test1", "test2"])

print(meta_talent)

print(meta_talent.to_yaml())
