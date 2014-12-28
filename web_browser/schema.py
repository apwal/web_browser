#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from yams.buildobjs import EntityType, String, SubjectRelation   
from cubicweb.schema import ERQLExpression
from cubes.rql_upload.schema  import CWUpload


###############################################################################
# Modification of the schema
###############################################################################

class CWProcessing(EntityType):
    """ An entity used to to processing status and results.

    Attributes
    ----------
    status: String (mandatory)
        the processing status, one of ('error', 'sucess', 'scheduled', 'running').
    result_form: SubjectRelation (mandatory)
        the link to the result form.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = {
        "read":   ("managers", ERQLExpression("X uploaded_by U"),),
        "add":    ("managers", "users"),
        "delete": ("managers",),
        "update": ("managers",),
    }

    # Entity parameters
    status = String(required=True, indexed=True,
                    vocabulary=("error", "sucess", "scheduled", "running"))

    # The link to the result data
    result_form = SubjectRelation(
        "UploadForm", cardinality="**", composite="subject")

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")


class ScoreValue(EntityType):
    """ An entity used to to store a parameter value.

    Attributes
    ----------
    name: String (mandatory)
        the parameter name.
    value: String (mandatory)
        the parameter value.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = {
        "read":   ("managers", ERQLExpression("X uploaded_by U"),),
        "add":    ("managers", "users"),
        "delete": ("managers",),
        "update": ("managers",),
    }

    # Entity parameters
    name = String(required=True, indexed=False)
    value = String(required=True, indexed=False)

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")


class ExternalResource(EntityType):
    """ An entity used to to store a file path.

    Attributes
    ----------
    name: String (mandatory)
        the parameter name.
    filepath: String (mandatory)
        the file path.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = {
        "read":   ("managers", ERQLExpression("X uploaded_by U"),),
        "add":    ("managers", "users"),
        "delete": ("managers",),
        "update": ("managers",),
    }

    # Entity parameters
    name = String(required=True, indexed=False)
    filepath = String(required=True, indexed=False)

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")


CWUpload.add_relation(
    SubjectRelation("CWProcessing", cardinality="1*", composite="subject"),
    name="related_processing")
CWProcessing.add_relation(
    SubjectRelation("ScoreValue", cardinality="**", composite="subject"),
    name="results")
CWProcessing.add_relation(
    SubjectRelation("ExternalResource", cardinality="**", composite="subject"),
    name="results")
