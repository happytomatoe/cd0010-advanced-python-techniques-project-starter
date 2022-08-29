"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    res = []
    with open(neo_csv_path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            res.append(NearEarthObject(row['pdes'], row['name'], row['diameter'], row['pha']))
    return res


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    res = []
    required_fields = ['des', 'cd', 'dist', 'v_rel']

    with open(cad_json_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        fields = data['fields']
        indexes = [fields.index(t) for t in required_fields]
        for approach in data['data']:
            res.append(CloseApproach(
                    approach[indexes[0]], approach[indexes[1]],
                    approach[indexes[2]], approach[indexes[3]]))
    return res
