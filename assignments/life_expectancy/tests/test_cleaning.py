"""Tests for the cleaning module"""
from unittest import mock

import pandas as pd
import pytest

from life_expectancy.cleaning import main


@pytest.mark.parametrize(
    "region, expected_fixture",
    [
        (None, "eu_life_expectancy_expected"),
        ("PT", "pt_life_expectancy_expected"),
    ],
)
def test_main(region, expected_fixture, request):
    """Test the main function for different regions."""
    # Retrieve the expected fixture using pytest's request object
    expected_output = request.getfixturevalue(expected_fixture)

    # Mock pd.DataFrame.to_csv
    with mock.patch.object(pd.DataFrame, "to_csv", return_value=None) as mock_to_csv:
        mock_to_csv.side_effect = lambda *args, **kwargs: print(
            "pd.DataFrame.to_csv called with:", args, kwargs
        )
        # Call the main function with the appropriate region
        actual_output = main(region)

        # Assert that to_csv was called once
        mock_to_csv.assert_called_once()

    # Assert that the actual output matches the expected output
    pd.testing.assert_frame_equal(actual_output, expected_output)
