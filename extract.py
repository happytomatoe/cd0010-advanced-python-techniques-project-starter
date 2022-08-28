"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # pdes - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
    # name - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
    # pha - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid,"
    # roughly meaning that it's large and can come quite close to Earth.
    # diameter - the NEO's diameter (from an equivalent sphere) in kilometers.

    res = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # //designation, name, diameter, hazardous
            res.append(NearEarthObject(row['pdes'], row['name'], row['diameter'], row['pha']))
    return res


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
    # orbit_id - orbit ID
    # jd - time of close-approach (JD Ephemeris Time)
    # cd - time of close-approach (formatted calendar date/time, in UTC)
    # dist - nominal approach distance (au)
    # dist_min - minimum (3-sigma) approach distance (au)
    # dist_max - maximum (3-sigma) approach distance (au)
    # v_rel - velocity relative to the approach body at close approach (km/s)
    # v_inf - velocity relative to a massless body (km/s)
    # t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes; days are not included if zero; example "13:02" is 13 hours 2 minutes; example "2_09:08" is 2 days 9 hours 8 minutes)
    # h - absolute magnitude H (mag)

    #

    # Test if there is an OOM
    res = []
    required_fields = ['des', 'cd', 'dist', 'v_rel']

    with open(cad_json_path, 'r') as f:
        data = json.load(f)
        fields = data['fields']
        indexes = [fields.index(t) for t in required_fields]
        for t in data['data']:
            res.append(CloseApproach(t[indexes[0]], t[indexes[1]], t[indexes[2]], t[indexes[3]]))
    return res
