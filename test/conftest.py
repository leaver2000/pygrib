"""Useful for testing."""

# stdlib
import os

# Local
import pygrib

# 3rd Party Import
import pytest


@pytest.fixture()
def samplegribfile(filename):
    """Open a grib file from the sampledata folder."""
    sampledir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "sampledata"
    )

    return pygrib.open(os.path.join(sampledir, filename))
