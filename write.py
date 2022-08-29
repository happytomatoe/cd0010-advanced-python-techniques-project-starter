"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.
"""
import csv
import json
from typing import Iterable

from models import CloseApproach


def write_to_csv(results: Iterable[CloseApproach], filename: str):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        # neo attributes
        'name',
        'diameter_km',
        'potentially_hazardous'
    )
    with open(filename, 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for approach in results:
            row = approach.serialize()
            if approach.neo:
                row.update(approach.neo.serialize())
            writer.writerow(row)


def write_to_json(results: Iterable[CloseApproach], filename: str):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    def serialize(approach: CloseApproach):
        res = approach.serialize()
        if approach.neo:
            res['neo'] = approach.neo.serialize()
        return res

    output = [serialize(r) for r in results]

    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(output, outfile)
