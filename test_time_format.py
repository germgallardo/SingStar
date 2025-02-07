# This file contains test cases for the `time_format` function to check different time duration formats to ensure they return the expected output
# For running the tests: pytest -v test_time_format.py
# The `-v` flag (verbose) is used for providing more details for each of the test cases during the execution

from test import time_format
import pytest


# The pytest.mark.parametrize decorator allows running the same `test_time_format` function with multiple test cases
# Each tuple contains the input (`duration`) for the `time_format` function and the expected output (`expected_output`)
# By using this decorator, the function will run consecutively according to the number of tuples that we define, in this case 6
# For more information: https://docs.pytest.org/en/stable/how-to/parametrize.html
@pytest.mark.parametrize("duration, expected_output", [
    ("PT1H4M3S", "1 hours 4 minutes 3 seconds"),
    ("PT11H50M20S", "11 hours 50 minutes 20 seconds"),
    ("PT07H04M02S", "07 hours 04 minutes 02 seconds"),
    ("PT7M23S", "7 minutes 23 seconds"),
    ("PT09M07S", "09 minutes 07 seconds"),
    ("PT27H03M11S", "27 hours 03 minutes 11 seconds")
])

def test_time_format(duration, expected_output):
    # with `assert` we can check if `duration` matches with the `expected_output`, if not it will raise an error and the test will fail
    assert time_format(duration) == expected_output