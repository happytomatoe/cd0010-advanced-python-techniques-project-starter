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
"""
from datetime import datetime
from typing import List

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

    designation: str
    name: str
    diameter: float
    hazardous: bool
    approaches: List

    def __init__(self, designation: str, name: str, diameter: str, hazardous: str, **info):
        """Create a new `NearEarthObject`.

        :param designation: the primary designation of the NEO.
        This is a unique identifier in the database, and its "name" to computer systems.

        :param name: the International Astronomical Union (IAU) name of the NEO.
         This is its "name" to humans.

        :param diameter: the NEO's diameter (from an equivalent sphere) in kilometers.

        :param hazardous: whether NASA has marked the NEO as a "Potentially Hazardous Asteroid",
         roughly meaning that it's large and can come quite close to Earth.
         "Y" is interpreted as True

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = designation
        self.name = name if name != '' else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = hazardous == 'Y'
        self.info = info
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})'

    def serialize(self):
        """Return object's view intended for serialization."""
        return {
            'designation': self.designation,
            'name': self.name if self.name else '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        is_hazardous = "is" if self.hazardous else "is not"
        return f"A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} km " \
               f"and {is_hazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    designation: str
    name: str
    time: datetime.date
    distance: float
    velocity: float
    neo: NearEarthObject

    def __init__(self, designation, calendar_date, distance, velocity, **info):
        """Create a new `CloseApproach`.

        :param designation: primary designation of the asteroid or comet
        :param calendar_date: time of close-approach (formatted calendar date/time, in UTC)
        :param distance: nominal approach distance (au)
        :param velocity: velocity relative to the approach body at close approach (km/s)
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = designation
        self.time = cd_to_datetime(calendar_date)
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.info = info
        self.neo = None

    @property
    def designation(self):
        """Primary designation of the asteroid or comet."""
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"A CloseApproach on {self.time_str} by '{self.designation}' " \
               f"at a distance of {self.distance:.2f} au " \
               f"and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """Return object's view intended for serialization."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'designation': self.designation
        }
