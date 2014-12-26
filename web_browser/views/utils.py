#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for details.
##########################################################################

# System import
import json
import os

# CW import
from cubicweb import ValidationError


def load_forms(cw_config, form_name):
    """ Function to load the forms structures from the file defined in the
    'menu_json' cubicweb instance parameter.

    Parameters
    ----------
    cw_config: dict
        the cubicweb configuration built from the instance 'all-in-one.conf'
        file.
    form_name: str
        the name of the registered form to be loaded.

    Returns
    -------
    config: dict
        the forms descriptions defined in the 'menu_json' setting
        file.
    """
    config_file = cw_config[form_name]
    if not os.path.isfile(config_file):
        raise ValidationError(
            "CWUpload", {
                "settings": unicode(
                    "cannot find the 'menu_json' "
                     "configuration file at location "
                    "'{0}'".format(config_file))})
    config = load_json(config_file)
    return byteify(config)


def load_json(json_file):
    """ Load a json file.

    Parameters
    ----------
    json_file: str
        the .json file to load.

    Returns
    -------
    struct: object
        the forms descriptions defined in the 'menu_json' setting
        file.
    """
    with open(json_file) as open_json:
        struct = json.load(open_json)
    return struct    


def byteify(struct):
    """ Convert unicode object to string object.

    Parameters
    ----------
    struct: object
        a python object that may contain unicode items.

    Returns
    -------
    clean_struct: object
        the same structure but with reencoded unicode items.
    """
    if isinstance(struct, dict):
        return {byteify(key): byteify(value) for key, value in struct.iteritems()}
    elif isinstance(struct, list):
        return [byteify(element) for element in struct]
    elif isinstance(struct, unicode):
        return struct.encode('utf-8')
    else:
        return struct
