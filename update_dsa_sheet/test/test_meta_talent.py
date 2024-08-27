from typing import Any

import pytest
from update_dsa_sheet.meta_talent import MetaTalent


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
