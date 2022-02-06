#!/usr/bin/env python3
#
# Create a pagerduty alert from the command line
#
# Copyright 2022, Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import argparse
import logging
import sys

from pdcrier.pagerduty import PagerDuty, loadCrierSettings


def parseCLI():
    """
    Parse the command line options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-token", help="PagerDuty api token", type=str)
    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        help="set log level",
        choices=["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"],
        default="INFO",
    )
    parser.add_argument(
        "--settings-file",
        "--settings",
        type=str,
        default="/config/pagerduty.yaml",
        help="Path to a settings file. Settings in the file are overridden by command line options",
    )
    # Alert options
    parser.add_argument(
        "--incident-key",
        help="Incident key - used to ensure no duplicate incidents. Will default to title if unset",
        type=str,
    )
    parser.add_argument(
        "--message",
        help="Alert message body - this won't be visible in SMSes",
        type=str,
    )
    parser.add_argument("--sender", help="Email address to send alerts from")
    parser.add_argument("--service-id", help="Service ID to create an alert")
    parser.add_argument(
        "--title",
        help="Title of alert - this is all you'll see via SMS, so be specific",
        type=str,
        required=True,
    )

    cli = parser.parse_args()
    loglevel = getattr(logging, cli.log_level.upper(), None)
    logFormat = "[%(asctime)s][%(levelname)8s][%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=loglevel, format=logFormat)
    logging.info("Set log level to %s", cli.log_level.upper())
    logging.debug(f"cli: {cli}")
    return cli


def alerter():
    """
    Create an alert
    """
    cli = parseCLI()
    settings = loadCrierSettings(cli=cli)
    if "incident_key" not in settings:
        logging.warning(f"incident_key not specified, using title '{cli.title}'")
        settings["incident_key"] = cli.title

    pd = PagerDuty(
        api_token=settings["pagerduty-api-token"], sender=settings["default-sender"]
    )
    incident = pd.createIncident(
        title=cli.title,
        service_id=settings["service_id"],
        incident_key=settings["incident_key"],
        message=cli.message,
    )
    try:
        logging.debug(f"Created incident {incident}.")
        logging.info(f"Incident title: {incident['title']}")
        logging.info(f"Incident number: {incident['incident_number']}")
        if "incident_key" in incident:
            logging.info(f"Incident key: {incident['incident_key']}")
        else:
            logging.debug("No incident key, allowing duplicates")
        logging.info(f"Description: {incident['description']}")
        logging.info(f"Created At: {incident['created_at']}")
    except KeyError:
        if "exception-response" in incident:
            error_status = 13
            error = incident["exception-response"].response.json()["error"]
            for error_message in error["errors"]:
                logging.warning(f"{error_message}")
                if (
                    error_message
                    == "Open incident with matching dedup key already exists on this service"
                ):
                    # We don't want shell scripts calling us to fail when an
                    # incident already exists, so we explicitly exit 0 when
                    # we find a duplicate.
                    error_status = 0
                    logging.warning("Do not need a new incident, one already exists.")
            if error_status != 0:
                logging.error("Could not create new incident!")
            sys.exit(error_status)


if __name__ == "__main__":
    print("This file should be imported, not run directly")
    alerter()
