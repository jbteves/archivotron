# Archivotron

[![Run Tests](https://github.com/jbteves/archivotron/actions/workflows/archivotron_actions.yaml/badge.svg)](https://github.com/jbteves/archivotron/actions/workflows/archivotron_actions.yaml)

## About

This is a package to allow the definition of a naming convention and use it to convert attributes of a file into the naming convention desired.
It can also convert a path of a given convention into the attributes.
This is mostly used to read BIDSish organization.

## Installation
To install from pypi, use
```
pip install archivotron
```

## Examples
In order to create a BIDSish name, you can use the following:

```python
from archivotron.bids import generate_bids

bids_tool = generate_bids()
```

You can then use the `bids_tool` object to serialize attributes into a file path:
```python
attributes = {
    "sub": "01",
    "ses": "pre",
    "modality": "anat",
    "suffix": "T1w",
}
print(bids_tool.gen_path(attributes))
sub-01/ses-pre/anat/sub-01_ses-pre_T1w
```

and serialize the same path into attributes:
```
print(bids_tool.into_attributes('sub-01/ses-pre/anat/sub-01_ses-pre_T1w'))
{'suffix': 'T1w', 'ses': 'pre', 'sub': '01', 'modality': 'anat'}
```
