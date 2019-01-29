#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals


import argparse
import shutil
import subprocess
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Docker image and run a " +
                                                 "Docker container with the specified options")
    parser.add_argument("image_name",
                        help="Name of the image to build",
                        metavar="IMAGE_NAME")
    parser.add_argument("image_version",
                        help="Version of the image to build",
                        metavar="IMAGE_VERSION")
    parser.add_argument("model_file",
                        help="Path to the model file.",
                        metavar="MODEL_FILE")
    parser.add_argument("test_file",
                        help="Path to the model's test data file.",
                        metavar="TEST_DATA_FILE")
    parser.add_argument("session_password",
                        help="Session password to run the container.",
                        metavar="SESSION_PASSWORD")
    parser.add_argument("--container-name",
                        default=None,
                        help="Name of the container to build (default: same as IMAGE_NAME)",
                        metavar="CONTAINER_NAME")
    parser.add_argument("--port-mapping",
                        default=80,
                        help="Port to map on the host machine to the container's application port",
                        metavar="PORT_MAPPING",
                        type=int)
    parser.add_argument("--json-log",
                        action="store_true",
                        help="Use json logging instead of journald logging.")
    parser.add_argument("--log-tag",
                        default="{{.ImageName}}/{{.Name}}/{{.ID}}",
                        help="Tag for the logs. Check https://docs.docker.com/config/containers/logging/log_tags/ " +
                             "for more information about it. Defaults to IMAGE_NAME/CONTAINER_NAME/CONTAINER_ID.")
    parser.add_argument("--log-max-size",
                        default=10,
                        help="Maximum log file size in Megabytes. " +
                             "Only valid with `--json-log` option. Defaults: 10 MB",
                        type=int)
    parser.add_argument("--log-max-file",
                        default=3,
                        help="Maximum number of log files. " +
                             "Only valid with `--json-log` option. Defaults: 3 files.",
                        type=int)
    args = parser.parse_args()

    if not args.json_log and shutil.which("journalctl") is None:
        print("You need to install journald for logging", file=sys.stderr)
        sys.exit(1)

    print("Building the Docker image", file=sys.stderr)
    build_command = list()
    build_command.append("docker build")
    build_command.append("-t %(image_name)s:%(image_version)s")
    build_command.append("--build-arg MODEL_FILE=%(model_file)s")
    build_command.append("--build-arg MODEL_TEST_FILE=%(test_file)s")
    build_command = " ".join(build_command)
    build_command = build_command % vars(args) + " ."
    subprocess.run(build_command, check=True, shell=True)

    print("\n\nRunning the Docker container", file=sys.stderr)
    run_command = list()
    run_command.append("docker run -d")
    run_command.append("-p %(port_mapping)d:80")
    run_command.append("-e SESSION_PASSWORD=%(session_password)s")

    if args.json_log:
        run_command.append("--log-driver=json-file")
        run_command.append("--log-opt max-size=%(log_max_size)dm")
        run_command.append("--log-opt max-file=%(log_max_file)d")
    else:
        run_command.append("--log-driver=journald")

    run_command.append("--log-opt tag=%(log_tag)s")
    run_command.append("--restart on-failure:5")
    run_command.append("--name %(container_name)s")
    run_command.append("%(image_name)s:%(image_version)s")
    run_command = " ".join(run_command)
    run_args = vars(args)
    if run_args["container_name"] is None:
        run_args["container_name"] = run_args["image_name"]
    run_command = run_command % run_args
    container_id = subprocess.run(run_command, check=True, shell=True,
                                  encoding="utf-8", stdout=subprocess.PIPE).stdout.strip()

    print("\n\nContainer running with ID %s and name %s" % (container_id[:12], run_args["container_name"]),
          file=sys.stderr)

    if args.json_log:
        log_files = subprocess.run("docker inspect -f  {{.LogPath}} %s" % container_id[:12],
                                   shell=True, check=True, encoding="utf-8",
                                   stdout=subprocess.PIPE).stdout.strip()
        print("Logfiles located at:\n%s" % log_files, file=sys.stderr)
    else:
        print("Logging by JournalD. You can check the logs for this container with " +
              "the following command:\n\tjournalctl CONTAINER_ID=%s" % container_id[:12], file=sys.stderr)
        print("You can check the logs for all the containers with the name %s " % run_args["container_name"] +
              "with the following command:\n\tjournalctl CONTAINER_NAME=%s" % run_args["container_name"],
              file=sys.stderr, end="\n\n")
        print("You should monitor your container with the `monitor-docker.py` script")

    print("Deployment finished", file=sys.stderr)
