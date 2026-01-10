from __future__ import annotations

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="session")
def resources_dir() -> Path:
    return Path(__file__).parent / "resources"


@pytest.fixture
def load_html(resources_dir: Path):
    def _load(name: str) -> str:
        return (resources_dir / name).read_text(encoding="utf8")

    return _load


@pytest.fixture
def load_soup(load_html):
    def _load(name: str) -> BeautifulSoup:
        return BeautifulSoup(load_html(name), "html.parser")

    return _load
