# -*- coding: utf-8 -*-
# Creator: Cristian Cardellino

from __future__ import absolute_import

import datetime
import os

from passlib.hash import pbkdf2_sha256 as sha256

from flask_app.utils import InvalidConfigurationError


LOGGING_CONFIG = {
    "version": 1,
    "formatters": {"default": {
        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    }},
    "handlers": {"wsgi": {
        "class": "logging.StreamHandler",
        "stream": "ext://flask.logging.wsgi_errors_stream",
        "formatter": "default"
    }},
    "root": {
        "level": "INFO",
        "handlers": ["wsgi"]
    }
}


def get_config_from_environment(logger):
    config = {}

    logger.info("Setting the configuration")
    # Get secret key from environment, otherwise generate one
    if os.environ.get("SECRET_KEY", None) is None:
        logger.warn("The SECRET_KEY environment variable is not set. Setting it to random.")
    config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(16))

    if os.environ.get("SECRET_KEY", None) is None:
        logger.warn("The JWT_SECRET_KEY environment variable is not set. Setting it to SECRET_KEY.")
    config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", config["SECRET_KEY"])

    # Get the default session expiration time (or set up otherwise)
    if os.environ.get("SESSION_EXPIRATION", None) is None:
        logger.warn("The SESSION_EXPIRATION environment variable is not set. Setting it to 24 hours.")
        config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=24)
    else:
        try:
            session_expiration = os.environ["SESSION_EXPIRATION"]
            config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=int(session_expiration))
        except ValueError:
            logger.warn("The SESSION_EXPIRATION environment variable is not a valid integer. " +
                        "Setting it to 24 hours.")
            config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=24)

    # Get password from environment or return error
    session_password = os.environ.get("SESSION_PASSWORD", None)
    if session_password is None:
        raise InvalidConfigurationError("The environment variable " +
                                        "\"SESSION_PASSWORD\" doesn't exist. " +
                                        "Please declare it before starting " +
                                        "this application.")
    else:
        config["SESSION_PASSWORD"] = sha256.hash(session_password)

    return config
