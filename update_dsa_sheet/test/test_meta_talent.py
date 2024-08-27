from typing import Any

import pytest
from update_dsa_sheet.meta_talent import MetaTalent, MetaTalentGroup


@pytest.fixture
def meta_talent_dict_with_upper_case_keys() -> dict[str, Any]:
    return {"namE": "Meta Talent", "TALEnts": ["Talent1", "Talent2"]}


@pytest.fixture
def meta_talent_dict() -> dict[str, Any]:
    return {"name": "Meta Talent", "talents": ["Talent1", "Talent2"]}


@pytest.fixture
def meta_talent() -> MetaTalent:
    return MetaTalent("Meta Talent", ["Talent1", "Talent2"])


@pytest.fixture
def meta_talent_yaml() -> str:
    return """
name: Meta Talent
talents:
- Talent1
- Talent2
"""


def test_deserialize_from_dict(
    meta_talent_dict_with_upper_case_keys: list[str, Any], meta_talent: MetaTalent
):
    actual = MetaTalent.from_dict(meta_talent_dict_with_upper_case_keys)
    print(actual)
    print("")
    print(meta_talent)
    assert meta_talent == actual


def test_serialize_to_dict(meta_talent_dict: dict[str, Any], meta_talent: MetaTalent):
    actual = meta_talent.to_dict()
    assert meta_talent_dict == actual


def test_deserialize_from_yaml(meta_talent: MetaTalent, meta_talent_yaml: str):
    actual = MetaTalent.from_yaml(meta_talent_yaml)
    assert meta_talent == actual


def test_serialize_to_yaml(meta_talent: MetaTalent, meta_talent_yaml: str):
    actual = meta_talent.to_yaml()
    assert meta_talent_yaml.strip() == actual.strip()


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
