from typing import Any

import pytest
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.meta_talent_group import MetaTalentGroup
from update_dsa_sheet.talents import Talents


@pytest.fixture
def meta_talent1() -> MetaTalent:
    return MetaTalent(
        "Meta Talent 1",
        ["Talent1", "Talent2"],
    )


@pytest.fixture
def meta_talent2() -> MetaTalent:
    return MetaTalent(
        "Meta Talent 2",
        ["Talent3", "Talent4"],
    )


@pytest.fixture
def meta_talent_group(meta_talent1, meta_talent2) -> MetaTalentGroup:
    return MetaTalentGroup(
        "Meta Talent Group",
        [
            meta_talent1,
            meta_talent2,
        ],
    )


class TestDictSerde:
    @pytest.fixture
    def meta_talent_group_dict_with_upper_case_keys(self) -> dict[str, Any]:
        return {
            "naME": "Meta Talent Group",
            "tALENts": [
                {"name": "Meta Talent 1", "talents": ["Talent1", "Talent2"]},
                {"name": "Meta Talent 2", "talents": ["Talent3", "Talent4"]},
            ],
        }

    @pytest.fixture
    def meta_talent_group_dict(self) -> dict[str, Any]:
        return {
            "name": "Meta Talent Group",
            "talents": [
                {"name": "Meta Talent 1", "talents": ["Talent1", "Talent2"]},
                {"name": "Meta Talent 2", "talents": ["Talent3", "Talent4"]},
            ],
        }

    def test_deserialize_group_from_dict(
        self,
        meta_talent_group: MetaTalentGroup,
        meta_talent_group_dict_with_upper_case_keys: dict[str, Any],
    ):
        actual = MetaTalentGroup.from_dict(meta_talent_group_dict_with_upper_case_keys)
        print(meta_talent_group)
        print("")
        print(actual)
        assert actual == meta_talent_group

    def test_serialize_group_to_dict(
        self,
        meta_talent_group_dict: dict[str, Any],
        meta_talent_group: MetaTalentGroup,
    ):
        actual = meta_talent_group.to_dict()
        assert actual == meta_talent_group_dict


class TestYamlSerde:

    @pytest.fixture
    def meta_talent_group_yaml(self) -> str:
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

    def test_serialize_group_to_yaml(
        self,
        meta_talent_group,
        meta_talent_group_yaml,
    ):
        actual = meta_talent_group.to_yaml()
        print(actual)
        print("")
        print(meta_talent_group_yaml)
        assert actual.strip() == meta_talent_group_yaml.strip()

    def test_deserialize_group_from_yaml(
        self,
        meta_talent_group,
        meta_talent_group_yaml,
    ):
        actual = MetaTalentGroup.from_yaml(meta_talent_group_yaml)
        assert actual == meta_talent_group


class TestSoup:
    @pytest.fixture
    def talents(self) -> Talents:
        return Talents(
            {
                "talent1": 1,
                "talent2": 2,
                "talent3": 3,
                "talent4": 4,
            }
        )

    @pytest.fixture
    def meta_talent_group_soup(
        self,
        meta_talent1,
        meta_talent2,
        talents,
    ) -> str:
        talent1: str = meta_talent1.to_soup(talents).prettify().strip()
        talent1: str = talent1.replace("\n", "\n  ")

        talent2: str = meta_talent2.to_soup(talents).prettify().strip()
        talent2: str = talent2.replace("\n", "\n  ")

        return f"""
<table class="talentgruppe gitternetz">
 <tbody>
  <tr>
   <th class="name">
    Meta Talent Group
   </th>
   <th class="formel">
    Formel
   </th>
   <th class="taw">
    TaW
   </th>
  </tr>
  {talent1}
  {talent2}
 </tbody>
</table>
"""

    def test_test(
        self,
        meta_talent_group_soup,
        meta_talent_group,
        talents,
    ):
        actual = meta_talent_group.to_soup(talents).prettify().strip()
        expected = meta_talent_group_soup.strip()

        assert actual == expected
