#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import argparse

from flask_app.app import create_app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run main API Flask server")
    parser.add_argument("--port",
                        type=int,
                        default=80,
                        help="Port to make the Flask server listen to. " +
                             "Defaults to 80, requires the user to have permissions.")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Activate debug mode for Flask server")

    args = parser.parse_args()

    app = create_app()
    app.run(host="0.0.0.0", debug=args.debug, port=args.port)

