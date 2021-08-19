# -*- coding: utf-8 -*-
"""
Helper Functions for different tests.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import math
import random


def allowed_value(client, field_id):
    """Creates and returns a value that is allowed for the given field_id."""
    # Get information on the field
    field = client.single_field(field_id)

    # Get the allowed values to update
    if field["field_type"] == "numeric":
        min_val = field["field_min"]
        max_val = field["field_max"]
        if min_val is None:
            min_val = 0
        if max_val is None:
            max_val = 99
        # Value needs to be between min_val and max_val
        # If they are floats, min_val needs to be rounded up and max_val rounded down.
        post_value = random.randint(int(math.ceil(min_val)), int(max_val))
    else:
        data_options = {
            "numeric": "1",
            "date": "11-11-2017",
            "string": "testing",
            "dropdown": "1",
            "radio": "1",
            "textarea": "testing",
            "slider": "5",
            "checkbox": "1",
            "calculation": "5",
            "year": "2005",
        }
        post_value = data_options[field["field_type"]]

    return post_value
