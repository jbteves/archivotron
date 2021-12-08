from archivotron import PathGenerator

import pytest

def test_constructor():
    """Makes sure the constructor works"""
    pg = PathGenerator("/data/tevesjb/my_project")
    assert pg is not None

def test_add_attribute():
    """Makes sure that add attribute has basic functionality"""
    # Verify we can add a normal attribute, should crash if not
    pg = PathGenerator("/")
    pg.add_attribute(
        "subject",
        str,
    )

    # Verify that adding an attribute that's a duplicate fails
    with pytest.raises(ValueError, match=r"^Attempted to overwrite*"):
        pg.add_attribute("subject", int)
