import os
import pytest

from src.data_mining.scrape_manufacturer_data import ManufacturerScraper
from .utils.fakes import FakeDB


@pytest.fixture(scope="module")
def makers():
    # Pass execution
    yield ManufacturerScraper().scrape_data_from_manufactures_catalog('c_container allmakes', FakeDB.CATALOG_URL)


@pytest.mark.parametrize("is_a_maker, expected_result", [
    ("", False),
    ("Moxy", True),
    ("Volvo", True)
])
def test_scraping_for_manufacturer_landing_page(makers, is_a_maker, expected_result):
    assert (is_a_maker in makers) == expected_result
