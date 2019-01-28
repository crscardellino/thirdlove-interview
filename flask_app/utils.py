# -*- coding: utf-8 -*-
# Creator: Cristian Cardellino

from __future__ import absolute_import


class ModelNotFoundError(Exception):
    pass


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def check_parameters(data):
    """
    Checks the parameters sent are correct. Raise InvalidUsage if not.
    :param data: JSON dictionary with parameters to run the recommendations.
    """
    valid_genders = {"M", "F", "O"}
    valid_occupations = {"administrator", "artist", "doctor", "educator",
                         "engineer", "entertainment", "executive", "healthcare",
                         "homemaker", "lawyer", "librarian", "marketing", "none",
                         "other", "programmer", "retired", "salesman",
                         "scientist", "student", "technician", "writer"}

    if "age" not in data.keys():
        raise InvalidUsage("Missing parameter: 'age'")
    elif not isinstance(data["age"], int):
        raise InvalidUsage("The parameter 'age' must be an integer")
    elif "gender" not in data.keys():
        raise InvalidUsage("Missing parameter: 'gender'")
    elif data['gender'] not in valid_genders:
        raise InvalidUsage("The parameter 'gender' must be one of the following: 'M', 'F', 'O'")
    elif "occupation" not in data.keys():
        raise InvalidUsage("Missing parameter: 'occupation'")
    elif data["occupation"] not in valid_occupations:
        raise InvalidUsage("The parameter 'occupation' must be one of the following: %s" %
                           ", ".join("'%s'" % o for o in sorted(valid_occupations)))
    elif not set(data.keys()).issubset({"age", "gender", "occupation"}):
        raise InvalidUsage("The only valid parameters are: 'age', 'gender', and 'occupation'")

    return data
