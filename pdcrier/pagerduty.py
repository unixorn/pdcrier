#!/usr/bin/env python3
#
# PagerDuty helper class and functions
#
# Copyright 2022, Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import logging

from pdcrier.utils import readYAMLFile
from pdpyras import APISession


def loadCrierSettings(cli):
    """
    Create a settings dict using a combination of values found in
    the settings YAML file and cli options.

    cli options override settings specified in the YAML file
    """
    settings = readYAMLFile(cli.settings_file)
    logging.debug(f"Raw settings: {settings}")

    if cli.api_token:
        settings["pagerduty-api-token"] = cli.api_token
    if not settings["pagerduty-api-token"]:
        logging.error(
            "You must specify a PagerDuty API token, either in the settings file or via the cli."
        )
        sys.exit(13)
    else:
        logging.debug(f"pagerduty-api-token: {settings['pagerduty-api-token']}")

    if cli.sender:
        settings["default-sender"] = cli.sender
    if not settings["default-sender"]:
        logging.error(
            "You must specify a default sender email address, either in the settings file or via the cli."
        )
        sys.exit(13)
    else:
        logging.debug(f"Default sender: {settings['default-sender']}")

    if cli.service_id:
        settings["service_id"] = cli.service_id
    if not settings["service_id"]:
        logging.error(
            "You must specify a PagerDuty service id, either in the settings file or via the cli."
        )
        sys.exit(13)
    else:
        logging.debug(f"Service ID: {settings['service_id']}")

    return settings


class PagerDuty:
    def __init__(self, api_token: str, sender: str):
        self.api_token = api_token
        self.session = APISession(self.api_token, default_from=sender)
        logging.debug(
            f"Set API token to {self.api_token}, default sender set to {sender}."
        )

    def createIncident(self, title: str, service_id: str, message: str = None):
        payload = {
            "type": "incident",
            "title": title,
            "service": {"id": service_id, "type": "service_reference"},
        }
        if message:
            logging.debug(f"Setting alert body to {message}")
            payload["body"] = {"type": "incident_body", "details": f"{message}"}
        else:
            logging.debug("No alert body set")
        logging.info(f"Creating an incident using payload {payload}")
        incident = self.session.rpost("incidents", json=payload)
        logging.debug(f"incident: {incident}")
        return incident


if __name__ == "__main__":
    import sys

    print("This is not meant to be run standalone. Import functions from it")
    sys.exit(13)
