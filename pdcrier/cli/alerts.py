#!/usr/bin/env python3
#
# Create a pagerduty alert
#
# Copyright 2022, Joe Block <jpb@unixorn.net>
# License: Apache 2.0

import argparse
import logging
import os

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
    if "HOME" in os.environ:
        parser.add_argument(
            "--settings-file",
            "--settings",
            type=str,
            help="Path to a settings file. Settings in the file are overridden by command line options",
            default=f"{os.environ.get('HOME')}/.hass-tools/pagerduty.yaml",
        )
    else:
        parser.add_argument(
            "--settings-file",
            "--settings",
            type=str,
            default="/config/pagerduty.yaml",
            help="Path to a settings file. Settings in the file are overridden by command line options",
        )

    # Alert options
    parser.add_argument(
        "--message",
        help="Alert message body - this won't be visible in SMSes",
        type=str,
    )
    parser.add_argument("--sender", help="Email address to send alerts from")
    parser.add_argument("--service-id", help="Service ID to create an alert")
    parser.add_argument(
        "--title",
        help="Title of alert - this is all you'll see via SMS",
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
    pd = PagerDuty(
        api_token=settings["pagerduty-api-token"], sender=settings["default-sender"]
    )
    incident = pd.createIncident(
        title=cli.title, service_id=settings["service_id"], message=cli.message
    )
    logging.debug(f"Created incident {incident}.")
    logging.info(f"Incident number: {incident['incident_number']}")
    logging.info(f"Incident title: {incident['title']}")
    logging.info(f"Description: {incident['description']}")
    logging.info(f"Created At: {incident['created_at']}")


if __name__ == "__main__":
    print("This file should be imported, not run directly")
    alerter()
