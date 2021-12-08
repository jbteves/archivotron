from archivotron import PathGenerator

import pytest

def test_constructor():
    pg = PathGenerator("/data/tevesjb/my_project")
    assert pg is not None

def test_add_attribute():
    # Verify we can add a normal attribute
    pg = PathGenerator("/")
    pg.add_attribute(
        "subject",
        str,
    )

    # Verify that adding an attribute that's a duplicate fails
    with pytest.raises(ValueError):
        pg.add_attribute("subject", int)
