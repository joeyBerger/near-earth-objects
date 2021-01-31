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
    
    neo_collection = []
    with open(neo_csv_path) as infile:
        reader = csv.DictReader(infile)
        for item in reader:
            if item["neo"] == "Y":
                neo = NearEarthObject(designation=item["pdes"],name=item["name"],diameter=item["diameter"],hazardous=item["pha"])
                neo_collection.append(neo)

    return neo_collection
    # return ()


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    ca_collection = []


    with open(cad_json_path) as infile:
        items = json.load(infile)
        data_ids = items["fields"]
        for data in items["data"]:
            ca = CloseApproach(designation=data[data_ids.index('des')],time=data[data_ids.index('cd')],distance=data[data_ids.index('dist')],velocity=data[data_ids.index('v_rel')],dist_min=data[data_ids.index('dist_min')],dist_max=data[data_ids.index('dist_max')])
            ca_collection.append(ca)

    return ca_collection
    # return ()
