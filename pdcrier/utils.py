#!/usr/bin/env python3
#
# Copyright 2022, Joe Block <jpb@unixorn.net>
# License: Apache 2.0
#
# Utility functions
import yaml


def writeYAMLFile(path: str, data):
    """
    Convert data to YAML and write it to path
    """
    file = open(path, "w")
    yaml.dump(data, file)
    file.close()


def readYAMLFile(path: str):
    """
    Read data from a YAML file
    """
    with open(path, "r") as file:
        # FullLoader handles the conversion from YAML scalar values to
        # Python dictionary format
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


if __name__ == "__main__":
    import sys

    print("This is not meant to be run standalone. Import functions from it")
    sys.exit(13)
