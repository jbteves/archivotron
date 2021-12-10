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
    _attribute_sep: str
        The attribute separatator. Default "_"
    _kv_sep: str
        The key-value separator. Default "-"

    Methods
    -------
    add_attribute
    add_level
    add_fname
    from
    """
    def __init__(
        self,
        root: str,
        attribute_sep: str = "_",
        kv_sep: str = "-",
    ) -> None:
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
        self._level_allowed = True
        self._attribute_sep = "_"
        self._kv_sep = "-"

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
        if name in self._attributes.keys():
            raise ValueError(
                f"Attempted to overwrite existing key {name}"
            )

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
        self._level_allowed = False

    def gen_path(self, attributes: dict) -> str:
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
            attribute is missing, or if there is no path target yet.
        TypeError, if there are any incorrect types
        """
        if self._level_allowed:
            raise ValueError("No path target completed!")

        for k, v in attributes.items():
            if k not in self._attributes:
                raise ValueError(f"Attribute {k} is not valid")

            type_required = self._attributes[k]["type"]
            type_received = type(v)

            if not isinstance(v, self._attributes[k]["type"]):
                raise TypeError(
                    f"Attribute type should be {type_required} for {k}, is "
                    f"{type_received}"
                )

        # Build the path
        path = ""
        for i in range(len(self._instructions)):
            instruction = self._instructions[i]
            val_only = self._instructions_val_only[i]
            print(f"{instruction}, {val_only}")

            if isinstance(instruction, str):
                instruction = [instruction]
            
            if val_only:
                path += self._attribute_sep.join(instruction)
            else:
                if isinstance(instruction, str):
                    atts = [instruction]
                else:
                    atts = instruction
                entries = []
                for att in atts:
                    entries.append(
                        f"{att}{self._kv_sep}{attributes[att]}"
                    )
                path += self._attribute_sep.join(entries)

        return path


class NameComponent:
    """Contains information to construct name components in a path,
    constructed from attribute key-value pairs.

    Attributes
    ----------
    key: str
        The key which is used
    val_type: type in (str, int)
        The type that the value should be
    kv_delim: str
        The delimeter between the key and value to be used
    value_only: bool
        Whether this namer should only display the value
    width: int
        The width to display a value with

    Methods
    -------
    name

    Examples
    --------
    1) Build a NameComponent with subject and ID, use defaults, print name
    >>> NameComponent("sub", str, "-").name({"sub": "Anthony"})
    'sub-Anthony'

    2) Build a NameComponent with subject and number, use defaults, specify
    a width for the session number
    >>> NameComponent("sub", int, "-", width=2).name({"sub": 1})
    'sub-01'

    3) Build a NameComponent with only a value
    >>> NameComponent("sub", int, None, width=2, value_only=True).name({"sub": 1})
    '01'
    """
    def __init__(
        self,
        key: str,
        val_type: type,
        kv_delim: str,
        value_only: bool = False,
        width: int = None
    ) -> None:
        self.key = key
        self.val_type = val_type
        self.kv_delim = kv_delim
        self.value_only = value_only
        self.width = width
    
    def name(self, attributes: dict) -> str:
        """Names a component from the given attributes

        Parameters
        ----------
        attributes: dict
            The dictionary which contains the key-value pair to use in
            order to name the component.

        Returns
        -------
        String representing the name component.
        """
        # Build the value component, which is always needed
        value = attributes[self.key]
        if self.width is not None:
            if self.val_type is str:
                value_component = f"{value:{self.width}}"
            elif self.val_type is int:
                value_component = f"{value:0{self.width}}"
        else:
            value_component = value
        # Add key component if needed
        if self.value_only:
            component = value_component
        else:
            component = self.key + self.kv_delim + value_component
        return component
