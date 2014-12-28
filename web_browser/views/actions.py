#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import re

# CW import
from cubicweb.web.action import Action
from cubicweb.predicates import is_instance
from cubicweb import ValidationError


###############################################################################
# Adaptors
###############################################################################

class ExternalResourceAdaptor(Action):
    """ Action to download entity objects related results.
    """
    __regid__ = "rqldownload-adaptors"
    __select__ = Action.__select__ & is_instance("CWProcessing")
    __rset_type__ = "jsonexport"

    def rql(self, rql, parameter_name):
        """ Method that patch the rql.

        note::
            The patched rql returned first elements are then the file pathes.
            Reserved keys are 'PATH', 'PROCESSING', 'SCORE'.
        """
        # Check that reserved keys are not used
        split_rql = re.split(r"[ ,]", rql)
        for revered_key in ["SCORE", "PATH"]:
            if revered_key in split_rql:
                raise ValidationError(
                    "CWSearch", {
                        "rql": _(
                            'cannot edit the rql "{0}", "{1}" is a reserved key, '
                            'choose another name'.format(rql, revered_key))})

        # Remove the begining of the rql in order to complete it
        formated_rql = " ".join(rql.split()[1:])

        # Complete the rql in order to access file pathes
        global_rql = ("Any PATH, {0}, {1} results SCORE, SCORE is ExternalResource, "
                      "SCORE filepath PATH".format(formated_rql, parameter_name))

        return global_rql


class ScoreValueAdaptor(Action):
    """ Action to download the score values.
    """
    __regid__ = "rqldownload-adaptors"
    __select__ = Action.__select__ & is_instance("CWUpload")
    __rset_type__ = "ecsvexport"

    def rql(self, rql, parameter_name):
        """ Method return the rql.
        """
        # Check that reserved keys are not used
        split_rql = re.split(r"[ ,]", rql)
        for revered_key in ["PROCESSING", "SCORE"]:
            if revered_key in split_rql:
                raise ValidationError(
                    "CWSearch", {
                        "rql": _(
                            'cannot edit the rql "{0}", "{1}" is a reserved key, '
                            'choose another name'.format(rql, revered_key))})

        # Remove the begining of the rql in order to complete it
        formated_rql = " ".join(rql.split()[1:])

        # Complete the rql in order to access file pathes
        global_rql = ("Any SCORE, {0}, {1} related_processing PROCESSING, "
                      "PROCESSING results SCORE, SCORE is ScoreValue".format(
                            formated_rql, parameter_name))

        return global_rql


###############################################################################
# Registration callback
###############################################################################

def registration_callback(vreg):
    vreg.register(ExternalResourceAdaptor)
    #vreg.register(ScoreValueAdaptor)
