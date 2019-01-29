#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals


import argparse
import getpass
import select
import smtplib
import subprocess
import sys


def get_email_server(server_address, server_port, email, password, is_secure):
    try:
        server = smtplib.SMTP(server_address, server_port)
        if is_secure:
            server.starttls()
        server.login(email, password)
        return server
    except Exception as e:
        print("Exception while connecting to server: %s" % e, file=sys.stderr)
        return None


def sendmail(server, email, message):
    msg = "There was an error on the server:\n\n%s" % message
    server.sendmail(email, email, msg)
    server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor docker container and " +
                                                 "alert on errors.")
    parser.add_argument("container_name",
                        help="Name of the container to monitor",
                        metavar="CONTAINER_NAME")
    parser.add_argument("smtp_server",
                        help="Server to use for sending the emails.",
                        metavar="SMTP_SERVER")
    parser.add_argument("email",
                        help="Email address to connect to the server.",
                        metavar="EMAIL")
    parser.add_argument("--print",
                        action="store_true",
                        help="Activate to print logs to STDOUT")
    parser.add_argument("--password",
                        default=None,
                        help="Password for the server. If not give will be asked.")
    parser.add_argument("--smtp-port",
                        default=25,
                        help="Port for the SMTP_SERVER.",
                        type=int)
    parser.add_argument("--is-secure",
                        action="store_true",
                        help="Whether to use a secure connection or not.")
    parser.add_argument("--notify-warnings",
                        action="store_true",
                        help="Notify warnings")

    args = parser.parse_args()

    monitor_command = "journalctl --lines 0 --follow CONTAINER_NAME=%s" % args.container_name
    monitor = subprocess.Popen(monitor_command.split(), stdout=subprocess.PIPE)
    poll = select.poll()
    poll.register(monitor.stdout)

    if args.password is not None:
        password = args.password
    else:
        password = getpass.getpass("Email %s - Password: " % args.email)

    print("Checking credentials", file=sys.stderr)
    if get_email_server(args.smtp_server, args.smtp_port, args.email,
                        password, args.is_secure) is None:
        sys.exit(1)

    print("Monitoring Docker container %s" % args.container_name, file=sys.stderr)

    while True:
        if poll.poll(1000):
            line = monitor.stdout.readline().decode("utf-8").strip()
            if args.print:
                print(line)
            if ("ERROR" in line) or ("WARNING" in line and args.notify_warnings):
                server = get_email_server(args.smtp_server, args.smtp_port,
                                          args.email, password, args.is_secure)
                sendmail(server, args.email, line)
