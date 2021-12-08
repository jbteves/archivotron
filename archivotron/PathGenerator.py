"""PathGenerator, contains definition for PathGenerator class"""

from typing import Union


class PathGenerator:
    """A class to generate paths from specified attributes

    Attributes
    ----------
    _root: str
        The path to the root of the relevant project
    _attributes: dict
        A dictionary of various attributes and their properties
    _instructions: list
        A list of instructions for constructing paths from attributes
    _instructions_val_only: list
        A list of booleans indicating whether instructions should print
        values only instead of key-value pairs
    _levels_allowed: bool
        Whether a level or fname may be appended

    Methods
    -------
    add_attribute
    add_level
    add_fname
    from
    """
    def __init__(self, root: str) -> None:
        """Constructs a new PathGenerator

        Parameters
        ----------
        root: str
            The root directory which all paths are relative to

        Returns
        -------
        None

        Raises
        ------
        TypeError, if anything is the wrong type
        """
        self._root = root
        self._attributes = {}
        self._instructions = []
        self._instructions_val_only = []
        self._levels_allowed = True
    def add_attribute(
        self,
        name: str,
        att_type: type,
        takes_value: bool = True, 
        required: bool = True,
    ) -> None:
        """Defines an attribute that could generate a path

        Parameters
        ----------
        name: str
            The name of the attribute
        type: type
            The expected type of the attribute
        takes_value: bool, optional
            Whether this attribute takes a value. Default True.
        required: bool, optional
            Whether this attribute is required to generate a name

        Returns
        -------
        None

        Raises
        ------
        TypeError, if anything is the wrong type
        """
        self._attributes[name] = {
            "takes_value": takes_value,
            "type": att_type,
            "required": required,
        }
    def add_level(
        self,
        attribute: Union[list, str],
        value_only: bool = False,
    ) -> None:
        """Defines a new level in the path

        Parameters
        ----------
        attribute: Union[list, str],
            If a string, the attribute which is used to define the name.
            If a list, the attributes to be joined to define the name.
        value_only: bool, optional
            Whether to ignore the attribute names and only use their
            values. Default False.

        Returns
        -------
        None

        Raises
        ------
        TypeError, if any incorrect types
        ValueError, if a filename was already defined
        """
        if not self._level_allowed:
            raise ValueError(
                "Attempted to define new level after fname defined!"
            )
        if isinstance(attribute, str):
            self._instructions.append([attribute])
        elif isinstance(attribute, list):
            self._instructions.append(
                [s for s in attribute]
            )
        else:
            raise TypeError(
                f"attribute should be str or list, is {type(attribute)}"
            )
        self._instructions_val_only.append(value_only)

    def add_fname(
        self,
        attributes: Union[list, str],
        value_only: bool = False
    ) -> None:
        """Defines the filename (prevents adding further levels)

        Parameters
        ----------
        attribute: Union[list, str],
            If a string, the attribute which is used to define the name.
            If a list, the attributes to be joined to define the name.
        value_only: bool, optional
            Whether to ignore the attribute names and only use their
            values. Default False.

        Returns
        -------
        None

        Raises
        ------
        TypeError, if any types incorrect
        ValueError, if a filename was already defined
        """
        if not self._level_allowed:
            raise ValueError(
                "Attempted to define a new filename after one was"
                " already defined!"
            )
        self.add_level(attributes, value_only)
        self._levels_allowed = False

    def from_att(self, attributes: dict) -> str:
        """Generates a full path from attribute dict

        Parameters
        ----------
        attributes: dict
            A dictionary of attributes and their values to generate the
            filename from.

        Returns
        -------
        A str representing the path to the file specified by the given
        attributes.

        Raises
        ------
        ValueError, if the attributes were not legal or a required
            attribute is missing.
        TypeError, if there are any incorrect types
        """
        return ""
