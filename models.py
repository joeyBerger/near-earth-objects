"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info["designation"]

        name = info.get("name", None)
        self.name = None if name == "" else name

        diameter = info.get("diameter", "nan")
        diameter = float("nan") if diameter == "" else float(diameter)
        self.diameter = diameter

        self.hazardous = True if info.get("hazardous", False) == "Y" else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def serialize(self, type="csv"):
        """Return a dictionary of needed properties associated with instance"""
        serilizable_dict = {}
        serilizable_dict["designation"] = self.designation
        serilizable_dict["name"] = (
            self.name if type == "csv" or self.name != None else ""
        )
        serilizable_dict["diameter_km"] = self.diameter
        serilizable_dict["potentially_hazardous"] = self.hazardous
        return serilizable_dict

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        name = "" if self.name == None else f" ({self.name})"
        return (self.designation + name)

    @property
    def hazardous_string(self):
        """Return a representation of the hazardous nature of this NEO"""
        qualifier = "" if self.hazardous else "not"
        return f"{qualifier} potentially hazardous"

    @property
    def diameter_string(self):
        """Return a representation of the diameter of this NEO"""
        return_string = (
            "an unknown diameter"
            if self.diameter == float("nan")
            else f"a diameter of {self.diameter:.3f} km"
        )
        return return_string

    def __str__(self):
        """Return `str(self description)`."""
        return f"NEO {self.fullname} has {self.diameter_string} and is {self.hazardous_string}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info["designation"]
        self.time = cd_to_datetime(info["time"])
        self.distance = float(info.get("distance", "nan"))
        self.velocity = float(info["velocity"])
        self.neo = None

    def serialize(self, type="csv"):
        """Return a dictionary of needed properties associated with instance"""
        serilizable_dict = {}
        serilizable_dict["datetime_utc"] = self.time_str
        serilizable_dict["distance_au"] = self.distance
        serilizable_dict["velocity_km_s"] = self.velocity
        if type == "json":
            serilizable_dict["neo"] = self.neo.serialize(type)

        return serilizable_dict

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def distance_string(self):
        """Return a representation of the distance of this CloseApproach"""
        return (
            ""
            if self.distance == float("nan")
            else f"at a distance of {self.distance:.2f} au"
        )

    @property
    def velocity_string(self):
        """Return a representation of the velocity of this CloseApproach"""
        return (
            ""
            if self.velocity == self.distance_string == ""
            else f"{self.velocity:.2f} km/s."
        )

    def __str__(self):
        """Return `str(self description)`."""
        return f"On {self.time_str}, '{self.neo.fullname}' approaches Earth {self.distance_string} and a velocity of {self.velocity_string}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
