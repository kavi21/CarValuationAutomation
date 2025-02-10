import time

import pandas as pd
import pytest

from pages.valuation_page import ValuationPage
from utils.file_reader import FileReader


@pytest.mark.parametrize(
    "registration", FileReader.read_reg_numbers("data/car_input.txt")
)
def test_car_valuation(setup_teardown, registration):
    driver = setup_teardown
    valuation_page = ValuationPage(driver)

    # Load the car valuation page
    valuation_page.load("https://motorway.co.uk/")

    # Enter car registration and fetch details
    valuation_page.enter_registration(registration)

    # Debugging pause (to ensure browser does not close immediately)
    time.sleep(5)

    actual_details = valuation_page.get_valuation_details()

    # Read expected data
    expected_results = FileReader.read_expected_results("data/car_output.csv")

    # Validate registration exists in expected results
    if registration not in expected_results.index:
        pytest.skip(f"Skipping test as {registration} is not in expected results")

    # Convert actual details to a pandas Series for comparison
    actual_series = pd.Series(
        {
            "MAKE_MODEL": actual_details.get("make_model", None),
            "YEAR": actual_details.get("year", None),
            "COLOR": actual_details.get("color", None),
            "FUEL_TYPE": actual_details.get("fuel_type", None),
        }
    )

    # Assert all details match expected data
    expected_series = expected_results.loc[registration]
    assert actual_series.equals(
        expected_series
    ), f"Expected: {expected_series}, Got: {actual_series}"


@pytest.mark.parametrize("registration", ["XX99 XXX", "1234 ABC", "XZ19 PQR"])
def test_invalid_registration(setup_teardown, registration):
    driver = setup_teardown
    valuation_page = ValuationPage(driver)

    valuation_page.load("https://motorway.co.uk/")
    valuation_page.enter_registration(registration)

    # Ensure error message appears
    assert (
        valuation_page.is_error_displayed()
    ), f"Expected error for invalid registration: {registration}"
