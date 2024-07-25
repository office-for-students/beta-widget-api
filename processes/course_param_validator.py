import logging
import re


def valid_course_params(params):

    if not mandatory_params_present(("institution_id", "course_id", "mode"), params):
        logging.error(f"Mandatory parameters missing from: {params}")
        return False

    if not valid_param("institution_id", params["institution_id"], 8, 8, r"[\d]+$"):
        return False

    if not valid_param("course_id", params["course_id"], 1, 30, r"[\w\~\-\(\)\!\$]+$"):
        return False

    if not valid_param("mode", params["mode"], 1, 1, r"[123]$"):
        return False

    return True


def mandatory_params_present(mandatory_params, params):
    return all(k in params for k in mandatory_params)


def valid_param(name, param, min_length, max_length, regex):
    """Test that the param looks reasonable."""

    if not StringValidator.is_valid_type(param):
        logging.error(f"{name} is an invalid type - expecting string")
        return False

    string_validator = StringValidator(
        param, min_length=min_length, max_length=max_length, regex=regex
    )

    if not string_validator.is_valid_length():
        logging.error(f"{name} is invalid length {param}")
        return False

    if not string_validator.valid_chars_only():
        logging.error(f"{param} the param for {name} contains invalid characters.")
        return False

    return True


class StringValidator:
    """Checks a string meets certain criteria

    Checks string meets caller's specified criteria
    in terms of type, length, and permitted chars.
    """

    def __init__(self, str_to_be_validated, min_length, max_length, regex):
        self.str_to_be_validated = str_to_be_validated
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex

    @staticmethod
    def is_valid_type(obj):
        return isinstance(obj, str)

    def is_valid_length(self):
        return self.min_length <= len(self.str_to_be_validated) <= self.max_length

    def valid_chars_only(self):
        return re.match(self.regex, self.str_to_be_validated) is not None
