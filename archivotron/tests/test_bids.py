from archivotron.bids import generate_bids


def test_generate_bids():
    """Tests for the bids generator; cloned from the other test"""
    bids = generate_bids()

    atts = {
        "sub": "01",
        "ses": "pre",
        "modality": "func",
        "task": "rest",
        "acq": "a",
        "ce": "a",
        "rec": "a",
        "dir": "PA",
        "run": "1",
        "echo": "1",
        "part": "mag",
        "suffix": "bold",
    }

    expected = (
        "sub-01/ses-pre/func/sub-01_ses-pre_"
        "task-rest_acq-a_ce-a_rec-a_run-1_dir-PA_echo-1_part-mag_bold"
    )

    assert bids.gen_path(atts) == expected
