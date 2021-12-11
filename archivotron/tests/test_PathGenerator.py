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
    pg.add_attribute("subject")

    # Verify that adding an attribute that's a duplicate fails
    with pytest.raises(ValueError, match=r"^Attempted to overwrite*"):
        pg.add_attribute("subject")


def test_gen_path_succeeds():
    """Tests for gen_path successes"""
    pg = PathGenerator("/")
    pg.add_attribute("subject")
    pg.add_attribute("session")
    pg.add_fname(["subject", "session"])

    atts = {
        "subject": "Jen",
        "session": "1",
    }

    assert pg.gen_path(atts) == "subject-Jen_session-1"

def test_gen_path_fails():
    """Tests for gen_path failures"""
    pg = PathGenerator("/")
    pg.add_attribute("subject")
    
    # Should fail because no path target
    with pytest.raises(ValueError, match=r"^No path target completed!"):
        pg.gen_path( { "subject": "Jen" } )

    pg.add_fname("subject")

    # Should fail because not a valid attribute
    with pytest.raises(ValueError, match=r"^Attribute pencils is not valid"):
        pg.gen_path( {"pencils": 5} )
