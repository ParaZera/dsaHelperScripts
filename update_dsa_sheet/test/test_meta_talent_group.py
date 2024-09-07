from typing import Any

import pytest
import yaml
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.meta_talent_group import MetaTalentGroup


@pytest.fixture
def meta_talent_group() -> MetaTalentGroup:
    return MetaTalentGroup(
        "Meta Talent Group",
        [
            MetaTalent("Meta Talent 1", ["Talent1", "Talent2"]),
            MetaTalent("Meta Talent 2", ["Talent3", "Talent4"]),
        ],
    )


@pytest.fixture
def meta_talent_group_dict() -> dict[str, Any]:
    return {
        "name": "Meta Talent Group",
        "talents": [
            {"name": "Meta Talent 1", "talents": ["Talent1", "Talent2"]},
            {"name": "Meta Talent 2", "talents": ["Talent3", "Talent4"]},
        ],
    }


@pytest.fixture
def meta_talent_group_dict_with_upper_case_keys() -> dict[str, Any]:
    return {
        "naME": "Meta Talent Group",
        "tALENts": [
            {"name": "Meta Talent 1", "talents": ["Talent1", "Talent2"]},
            {"name": "Meta Talent 2", "talents": ["Talent3", "Talent4"]},
        ],
    }


@pytest.fixture
def meta_talent_group_yaml() -> str:
    return """
name: Meta Talent Group
talents:
- name: Meta Talent 1
  talents:
  - Talent1
  - Talent2
- name: Meta Talent 2
  talents:
  - Talent3
  - Talent4\n
"""


def test_deserialize_group_from_dict(
    meta_talent_group: MetaTalentGroup,
    meta_talent_group_dict_with_upper_case_keys: dict[str, Any],
):
    actual = MetaTalentGroup.from_dict(meta_talent_group_dict_with_upper_case_keys)
    print(meta_talent_group)
    print("")
    print(actual)
    assert actual == meta_talent_group


def test_serialize_group_to_dict(meta_talent_group_dict, meta_talent_group):
    actual = meta_talent_group.to_dict()
    assert actual == meta_talent_group_dict


def test_serialize_group_to_yaml(meta_talent_group, meta_talent_group_yaml):
    actual = meta_talent_group.to_yaml()
    print(actual)
    print("")
    print(meta_talent_group_yaml)
    assert actual.strip() == meta_talent_group_yaml.strip()


def test_deserialize_group_from_yaml(meta_talent_group, meta_talent_group_yaml):
    actual = MetaTalentGroup.from_yaml(meta_talent_group_yaml)
    assert actual == meta_talent_group


# def test_temp_stuff(meta_talent_group):
#     a = [meta_talent_group.to_dict(), meta_talent_group.to_dict()]

#     y = yaml.dump(a)

#     print(y)

#     assert False


# def test_asdf(meta_talent_group_yaml):
#     y = """- name: Meta Talent Group
#   talents:
#   - name: Meta Talent 1
#     talents: &id001
#     - Talent1
#     - Talent2
#   - name: Meta Talent 2
#     talents: &id002
#     - Talent3
#     - Talent4
# - name: Meta Talent Group
#   talents:
#   - name: Meta Talent 1
#     talents: *id001
#   - name: Meta Talent 2
#     talents: *id002
# """

#     a = yaml.load(y, Loader=yaml.FullLoader)
#     print(a)

#     b = []

#     for i in a:
#         b.append(MetaTalentGroup.from_dict(i))

#     print(b)

#     c = yaml.load(meta_talent_group_yaml, Loader=yaml.FullLoader)

#     if isinstance(c, list):
#         print("Is List")

#     if isinstance(c, dict):
#         print("Is Dict")

#     for i in c:
#         print("ASD")
#         print(i)

#     assert False
