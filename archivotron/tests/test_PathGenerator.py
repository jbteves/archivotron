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
    pg = PathGenerator()
    # Set attributes
    pg.add_attribute("subject")
    pg.add_attribute("session")
    # Build path
    pg.add_component("subject")
    pg.add_filesep()
    pg.add_component("session")
    pg.add_filesep()
    pg.add_component("modality", value_only=True)
    pg.add_filesep()
    pg.add_component("subject")
    pg.add_component("session")
    pg.add_component("submodality", value_only=True)
    pg.terminate()

    atts = {
        "subject": "Jen",
        "session": "1",
        "modality": "anat",
        "submodality": "T1w"
    }

    expected = (
        "/subject-Jen"
        "/session-1"
        "/anat"
        "/subject-Jen_session-1_T1w"
    )
    assert pg.gen_path(atts) == expected

    af = PathGenerator(None, attribute_sep=".", kv_sep="")
    # Set attributes
    af.add_attribute("pb")
    af.add_attribute("subj")
    af.add_attribute("r")
    af.add_attribute("step")
    af.add_attribute("space")
    # Build path
    af.add_component("pb")
    af.add_component("subj")
    af.add_component("r")
    af.add_component("step", value_only=True)
    af.delimiter_override("+")
    af.add_component("space", value_only=True)
    af.terminate()

    atts = {
        "pb": "01",
        "subj": "99",
        "r": "01",
        "step": "tshift",
        "space": "orig",
    }

    expected = "pb01.subj99.r01.tshift+orig"

    assert af.gen_path(atts) == expected


def test_gen_path_fails():
    """Tests for gen_path failures"""
    pg = PathGenerator("/")
    pg.add_attribute("subject")

    # Should fail because no path target
    with pytest.raises(ValueError, match=r"^No path target completed!*"):
        pg.gen_path({"subject": "Jen"})

    pg.add_component("subject")
    pg.terminate()

    # Should fail because not a valid attribute
    with pytest.raises(ValueError, match=r"^Attribute pencils is not valid"):
        pg.gen_path({"pencils": 5})
