"""PathGenerator, contains definition for PathGenerator class"""

from typing import Union

import os


class PathGenerator:
    """A class to generate paths from specified attributes

    Attributes
    ----------
    _attributes: dict
        A dictionary of various attributes and their properties
    _components: list(NameComponent)
        A list of naming components
    _terminated: bool
        Whether this object's builder pattern has terminated
    _attribute_sep: str
        The attribute separatator. Default "_"
    _kv_sep: str
        The key-value separator. Default "-"
    _file_sep: str
        The file separator. Default is platform-specific from os.path.

    Methods
    -------
    add_attribute
    add_level
    add_fname
    from
    """
    def __init__(
        self,
        root: str = "",
        attribute_sep: str = "_",
        kv_sep: str = "-",
        file_sep: str = None,
    ) -> None:
        """Constructs a new PathGenerator

        Parameters
        ----------
        root: str
            The root directory which all paths are relative to
        attribute_sep: str, optional
            The default delimeter for attributes. Default "_".
        kv_sep: str, optional
            The default delimiter for key-value pairs. Default "-".
        file_sep: str, optional
            The default delimeter for file paths. Default system-dependent.
            ADMONITION: unless you are writing code for another machine, it
            you should probably not override this.

        Returns
        -------
        None

        Raises
        ------
        TypeError, if anything is the wrong type
        """
        self._attributes = {}
        self._terminated = False
        self._attribute_sep = attribute_sep
        self._kv_sep = kv_sep
        if file_sep is None:
            self._file_sep = os.path.sep
        elif file_sep in ("/", "\\"):
            self._file_sep = file_sep
        else:
            raise ValueError(
                f"Specified file separator {file_sep} is not valid for most"
                " machines, terminating execution."
            )
        if root is None:
            self._components = []
        elif root == "":
            self._components = [self._file_sep]
        else:
            self._components = [root + self._file_sep]

    def add_attribute(
        self,
        name: str,
        takes_value: bool = True,
        required: bool = True,
    ) -> None:
        """Defines an attribute that could generate a path

        Parameters
        ----------
        name: str
            The name of the attribute
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
            "required": required,
        }

    def add_component(
        self,
        key: str,
        delimiter: str = None,
        value_only: bool = False,
    ) -> None:
        """Adds a name component to the path to generate

        Parameters
        ----------
        key: str
            The key that this component will use
        delimiter: str, optional
            The delimiter that this component will use. Default is to use
            the path generator's kvsep attribute. Use "" to indicate no
            delimeter. This value is ignored if value_only is True.
        value_only: bool, optional
            Whether this name component will print only the value.
        """
        if delimiter is None:
            delimiter = self._kv_sep
        nc = NameComponent(key, delimiter, value_only=value_only)
        # We have to make sure we don't have 0 elements, or else we'll have
        # an index error.
        if len(self._components) == 0:
            self._components.append(nc)
        elif isinstance(self._components[-1], NameComponent):
            # Insert the default delimiter between components
            self._components.append(self._attribute_sep)
            self._components.append(nc)
        else:
            # We already have an overridden delimiter, no need to add the
            # default delimiter
            self._components.append(nc)

    def delimiter_override(self, delimiter: str) -> None:
        """Adds a delimiter override

        Parameters
        ----------
        delimiter: str
            The delimiter to override with
        """
        self._components.append(delimiter)

    def add_filesep(self):
        """Adds a file separator to the name component list"""
        self._components.append(self._file_sep)

    def terminate(self):
        """Terminate the build pattern"""
        self._terminated = True

    def gen_path(self, attributes: dict) -> str:
        """Generate a path with this generator and an attribute dict

        Parameters
        ----------
        attributes: dict
            The attributes to use for this path generator

        Raises
        ------
        ValueError if one of the attributes was not supplied to this path
            generator.
        """
        if not self._terminated:
            raise ValueError(
                "No path target completed!"
                "Use the terminate_path method to terminate the builder."
            )

        try:
            path = "".join(
                [PathGenerator._str(x, attributes) for x in self._components]
            )
        except KeyError:
            # Apparently KeyError doesn't retain which key failed
            for k in attributes.keys():
                if k not in self._attributes.keys():
                    raise ValueError(f"Attribute {k} is not valid")

        return path

    def _str(o: Union[str, "NameComponent"], att: dict) -> str:
        """Ingests a string or name component and returns a string

        Parameters
        ----------
        o: str | NameComponent
            The object to turn into a string
        att: dict
            The attribute dictionary, in case the object is a NameComponent

        Returns
        -------
        The string representation of the object
        """

        if isinstance(o, str):
            return o
        elif isinstance(o, NameComponent):
            return o.name(att)


class NameComponent:
    """Contains information to construct name components in a path,
    constructed from attribute key-value pairs.

    Attributes
    ----------
    key: str
        The key which is used
    kv_delim: str
        The delimeter between the key and value to be used
    value_only: bool
        Whether this namer should only display the value

    Methods
    -------
    name

    Examples
    --------
    1) Build a NameComponent with subject and ID, use defaults, print name
    >>> NameComponent("sub", "-").name({"sub": "Anthony"})
    'sub-Anthony'

    2) Build a NameComponent with only a value
    >>> NameComponent("sub", None, value_only=True).name({"sub": "01"})
    '01'
    """
    def __init__(
        self,
        key: str,
        kv_delim: str,
        value_only: bool = False,
    ) -> None:
        self.key = key
        self.kv_delim = kv_delim
        self.value_only = value_only

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
        # Add key component if needed
        if self.value_only:
            component = value
        else:
            component = self.key + self.kv_delim + value
        return component
