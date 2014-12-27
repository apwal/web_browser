#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Define global parameter
CONVERSION_TYPES = {}


###############################################################################
# Registration callback
###############################################################################

def registration_callback(vreg):
    """ The authorized field conversion are registered from this function.

    The registration identifier must be of the form "<class_name>".
    The preregistered fields are:

    * Basic fields: StringField - IntField - FloatField - BooleanField.

    * Compound fields: FileField.
    """

    # Got through fields we want to register
    for field_name in ["StringField", "FileField"]:

        # Define class parameters
        CONVERSION_TYPES[field_name] = str

    CONVERSION_TYPES["IntField"] = int
    CONVERSION_TYPES["FloatField"] = float
    CONVERSION_TYPES["BooleanField"] = bool

