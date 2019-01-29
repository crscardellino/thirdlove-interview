# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import argparse
import json
import logging
import sys

from sklearn.externals import joblib


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to run accuracy tests over the model.")
    parser.add_argument("model_file",
                        help="Path to the model file.")
    parser.add_argument("test_file",
                        help="Path to test file.")
    parser.add_argument("--error-tolerance",
                        type=float,
                        default=1e-5,
                        help="Error tolerance for the model score.")

    args = parser.parse_args()

    logFormatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    logger.info("Loading model from %s" % args.model_file)
    model = joblib.load(args.model_file)

    logger.info("Loading test data from %s" % args.test_file)
    with open(args.test_file, "r") as fh:
        test_data = json.load(fh)

    logger.info("Checking scores")
    model_score = model.score(test_data["data"], test_data["target"])
    if model_score < (test_data["expected_score"] - args.error_tolerance):
        logger.error("The model score is less than the expected score")
        sys.exit(1)

    logger.info("Accuracy test finished successfully")

