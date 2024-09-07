from typing import Any

import pytest
from update_dsa_sheet.meta_talent import MetaTalent
from update_dsa_sheet.talents import Talents


@pytest.fixture
def meta_talent() -> MetaTalent:
    return MetaTalent(
        "Meta Talent",
        ["Talent1", "Talent2"],
    )


class TestDictSerde:
    @pytest.fixture
    def meta_talent_dict_with_upper_case_keys(self) -> dict[str, Any]:
        return {
            "namE": "Meta Talent",
            "TALEnts": ["Talent1", "Talent2"],
        }

    @pytest.fixture
    def meta_talent_dict(self) -> dict[str, Any]:
        return {
            "name": "Meta Talent",
            "talents": ["Talent1", "Talent2"],
        }

    def test_deserialize_from_dict(
        self,
        meta_talent: MetaTalent,
        meta_talent_dict_with_upper_case_keys: dict[str, Any],
    ):
        actual = MetaTalent.from_dict(meta_talent_dict_with_upper_case_keys)
        print(actual)
        print("")
        print(meta_talent)
        assert meta_talent == actual

    def test_serialize_to_dict(
        self,
        meta_talent: MetaTalent,
        meta_talent_dict: dict[str, Any],
    ):
        actual = meta_talent.to_dict()
        assert meta_talent_dict == actual


class TestYamlSerde:
    @pytest.fixture
    def meta_talent_yaml(self) -> str:
        return """name: Meta Talent
talents:
- Talent1
- Talent2
"""

    def test_deserialize_from_yaml(
        self,
        meta_talent: MetaTalent,
        meta_talent_yaml: str,
    ):
        actual = MetaTalent.from_yaml(meta_talent_yaml)
        expected: MetaTalent = meta_talent
        assert expected == actual

    def test_serialize_to_yaml(
        self,
        meta_talent: MetaTalent,
        meta_talent_yaml: str,
    ):
        actual = meta_talent.to_yaml().strip()
        expected = meta_talent_yaml.strip()
        assert expected == actual


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
    def meta_talent_simple_soup(self) -> str:
        return """<tr>
 <td class="name">
  Meta Talent
 </td>
 <td class="formel">
  (Talent1 + Talent2) / 2
 </td>
 <td class="taw">
  1
 </td>
</tr>"""

    def test_simple_soup(
        self,
        talents: Talents,
        meta_talent: MetaTalent,
        meta_talent_simple_soup: str,
    ):
        actual = meta_talent.to_soup(talents).prettify()
        print("actual:")
        print(actual)
        print("=============")
        print("expected:")
        print(meta_talent_simple_soup)
        assert meta_talent_simple_soup.strip() == actual.strip()
